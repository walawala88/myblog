from flask import jsonify, request, send_from_directory
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, verify_jwt_in_request
from datetime import datetime, timedelta
import os
import requests as http_requests
from app import app, db
from models import User, Category, Tag, Post, Comment, Visitor, Like, Gallery, Honor, SiteSetting, MubuNote, Movie, Music
from config import Config
from oss_utils import get_oss_storage

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data.get('username')).first()
    if user and user.check_password(data.get('password')):
        access_token = create_access_token(identity=str(user.id), expires_delta=timedelta(hours=24))
        return jsonify({'access_token': access_token, 'user': {'id': user.id, 'username': user.username}})
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/posts', methods=['GET'])
def get_posts():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    category_id = request.args.get('category_id', type=int)
    tag_id = request.args.get('tag_id', type=int)
    search = request.args.get('search')
    
    query = Post.query.filter_by(is_published=True)
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    if tag_id:
        query = query.join(Post.tags).filter(Tag.id == tag_id)
    if search:
        query = query.filter((Post.title.contains(search)) | (Post.content.contains(search)))
    
    posts = query.order_by(Post.is_top.desc(), Post.created_at.desc()).paginate(page=page, per_page=per_page)
    
    return jsonify({
        'posts': [{
            'id': p.id,
            'title': p.title,
            'slug': p.slug,
            'excerpt': p.excerpt,
            'category': p.category.name if p.category else None,
            'tags': [t.name for t in p.tags],
            'views': p.views,
            'likes': p.likes,
            'created_at': p.created_at.isoformat()
        } for p in posts.items],
        'total': posts.total,
        'pages': posts.pages
    })

@app.route('/api/posts/<slug>', methods=['GET'])
def get_post(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    post.views += 1
    db.session.commit()
    
    comments = Comment.query.filter_by(post_id=post.id, parent_id=None, is_approved=True, is_spam=False).all()
    
    return jsonify({
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'category': post.category.name if post.category else None,
        'tags': [t.name for t in post.tags],
        'views': post.views,
        'likes': post.likes,
        'created_at': post.created_at.isoformat(),
        'updated_at': post.updated_at.isoformat(),
        'comments': [{
            'id': c.id,
            'author_name': c.author_name,
            'content': c.content,
            'created_at': c.created_at.isoformat(),
            'replies': [{
                'id': r.id,
                'author_name': r.author_name,
                'content': r.content,
                'created_at': r.created_at.isoformat()
            } for r in c.replies if r.is_approved and not r.is_spam]
        } for c in comments]
    })

@app.route('/api/posts', methods=['POST'])
@jwt_required()
def create_post():
    data = request.get_json()
    category_id = data.get('category_id')
    if category_id == '' or category_id is None:
        category_id = None
    
    post = Post(
        title=data['title'],
        slug=data['slug'],
        content=data['content'],
        excerpt=data.get('excerpt'),
        category_id=category_id,
        author_id=int(get_jwt_identity()),
        is_published=data.get('is_published', False),
        is_draft=data.get('is_draft', True),
        is_top=data.get('is_top', False)
    )
    
    if data.get('tags'):
        for tag_name in data['tags']:
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name, slug=tag_name.lower().replace(' ', '-'))
                db.session.add(tag)
            post.tags.append(tag)
    
    db.session.add(post)
    db.session.commit()
    return jsonify({'message': 'Post created', 'id': post.id}), 201

@app.route('/api/posts/<int:id>', methods=['PUT'])
@jwt_required()
def update_post(id):
    data = request.get_json()
    post = Post.query.get_or_404(id)
    post.title = data.get('title', post.title)
    post.slug = data.get('slug', post.slug)
    post.content = data.get('content', post.content)
    post.excerpt = data.get('excerpt', post.excerpt)
    category_id = data.get('category_id', post.category_id)
    if category_id == '':
        category_id = None
    post.category_id = category_id
    post.is_published = data.get('is_published', post.is_published)
    post.is_draft = data.get('is_draft', post.is_draft)
    post.is_top = data.get('is_top', post.is_top)
    
    if data.get('tags'):
        post.tags.clear()
        for tag_name in data['tags']:
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name, slug=tag_name.lower().replace(' ', '-'))
                db.session.add(tag)
            post.tags.append(tag)
    
    db.session.commit()
    return jsonify({'message': 'Post updated'})

@app.route('/api/posts/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_post(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Post deleted'})

@app.route('/api/admin/posts', methods=['GET'])
@jwt_required()
def get_admin_posts():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    
    posts = Post.query.order_by(Post.is_top.desc(), Post.created_at.desc()).paginate(page=page, per_page=per_page)
    
    return jsonify({
        'posts': [{
            'id': p.id,
            'title': p.title,
            'slug': p.slug,
            'excerpt': p.excerpt,
            'content': p.content,
            'category': p.category.name if p.category else None,
            'category_id': p.category_id,
            'tags': [t.name for t in p.tags],
            'views': p.views,
            'likes': p.likes,
            'is_published': p.is_published,
            'is_draft': p.is_draft,
            'is_top': p.is_top,
            'created_at': p.created_at.isoformat()
        } for p in posts.items],
        'total': posts.total,
        'pages': posts.pages
    })

@app.route('/api/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'slug': c.slug,
        'description': c.description,
        'count': len(c.posts)
    } for c in categories])

@app.route('/api/categories', methods=['POST'])
@jwt_required()
def add_category():
    data = request.get_json()
    cat = Category(
        name=data['name'],
        description=data.get('description', '')
    )
    db.session.add(cat)
    db.session.commit()
    return jsonify({'message': 'Category added', 'id': cat.id}), 201

@app.route('/api/tags', methods=['GET'])
def get_tags():
    tags = Tag.query.all()
    return jsonify([{
        'id': t.id,
        'name': t.name,
        'slug': t.slug,
        'count': len(t.posts)
    } for t in tags])

@app.route('/api/comments', methods=['POST'])
def create_comment():
    data = request.get_json()
    comment = Comment(
        post_id=data['post_id'],
        parent_id=data.get('parent_id'),
        author_name=data['author_name'],
        author_email=data.get('author_email'),
        content=data['content'],
        is_approved=True
    )
    db.session.add(comment)
    db.session.commit()
    return jsonify({'message': 'Comment created'}), 201

@app.route('/api/comments', methods=['GET'])
def get_all_comments():
    comments = Comment.query.filter_by(parent_id=None).order_by(Comment.created_at.desc()).all()
    return jsonify([{
        'id': c.id,
        'author_name': c.author_name,
        'content': c.content,
        'created_at': c.created_at.isoformat(),
        'replies': [{
            'id': r.id,
            'author_name': r.author_name,
            'content': r.content,
            'created_at': r.created_at.isoformat()
        } for r in c.replies if r.is_approved and not r.is_spam]
    } for c in comments])

@app.route('/api/comments/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_comment(id):
    comment = Comment.query.get_or_404(id)
    db.session.delete(comment)
    db.session.commit()
    return jsonify({'message': 'Comment deleted'})

@app.route('/api/posts/<int:id>/like', methods=['POST'])
def like_post(id):
    user_ip = request.remote_addr
    existing_like = Like.query.filter_by(post_id=id, user_ip=user_ip).first()
    
    if existing_like:
        db.session.delete(existing_like)
        Post.query.get(id).likes -= 1
        db.session.commit()
        return jsonify({'liked': False})
    else:
        like = Like(post_id=id, user_ip=user_ip)
        db.session.add(like)
        Post.query.get(id).likes += 1
        db.session.commit()
        return jsonify({'liked': True})

@app.route('/api/archive', methods=['GET'])
def get_archive():
    posts = Post.query.filter_by(is_published=True).order_by(Post.created_at.desc()).all()
    archive = {}
    for post in posts:
        key = post.created_at.strftime('%Y-%m')
        if key not in archive:
            archive[key] = []
        archive[key].append({
            'id': post.id,
            'title': post.title,
            'slug': post.slug,
            'created_at': post.created_at.isoformat()
        })
    return jsonify(archive)

@app.route('/api/visitor', methods=['POST'])
def track_visitor():
    data = request.get_json()
    ip = request.remote_addr
    cutoff_time = datetime.utcnow() - timedelta(minutes=30)
    recent_visit = Visitor.query.filter(
        Visitor.ip_address == ip,
        Visitor.visited_at >= cutoff_time
    ).first()
    if recent_visit:
        return jsonify({'message': 'Already tracked', 'skipped': True})
    visitor = Visitor(
        ip_address=ip,
        user_agent=request.user_agent.string,
        page_url=data.get('page_url', '')
    )
    db.session.add(visitor)
    db.session.commit()
    return jsonify({'message': 'Visitor tracked'})

@app.route('/api/visitors', methods=['GET'])
@jwt_required()
def get_visitors():
    page = request.args.get('page', 1, type=int)
    visitors = Visitor.query.order_by(Visitor.visited_at.desc()).paginate(page=page, per_page=20)
    return jsonify({
        'visitors': [{
            'id': v.id,
            'ip_address': v.ip_address,
            'user_agent': v.user_agent,
            'page_url': v.page_url,
            'visited_at': v.visited_at.isoformat()
        } for v in visitors.items],
        'total': visitors.total
    })

@app.route('/api/messages', methods=['GET'])
def get_messages():
    comments = Comment.query.order_by(Comment.created_at.desc()).all()
    return jsonify([{
        'id': c.id,
        'name': c.author_name or '匿名',
        'content': c.content,
        'created_at': c.created_at.isoformat()
    } for c in comments])

@app.route('/api/messages', methods=['POST'])
def add_message():
    data = request.get_json()
    comment = Comment(
        post_id=data.get('post_id', 1),
        author_name=data.get('name', '匿名'),
        content=data.get('content', ''),
        is_approved=True
    )
    db.session.add(comment)
    db.session.commit()
    return jsonify({'message': 'Comment added', 'name': comment.author_name, 'content': comment.content}), 201

@app.route('/api/stats', methods=['GET'])
def get_stats():
    post_count = Post.query.filter_by(is_published=True).count()
    comment_count = Comment.query.filter_by(is_approved=True, is_spam=False).count()
    visitor_count = Visitor.query.count()
    like_count = SiteSetting.query.filter_by(key='blogger_likes').first()
    return jsonify({
        'posts': post_count,
        'comments': comment_count,
        'visitors': visitor_count,
        'likes': int(like_count.value) if like_count else 0
    })

@app.route('/api/blogger/like', methods=['POST'])
def blogger_like():
    like_count = SiteSetting.query.filter_by(key='blogger_likes').first()
    if not like_count:
        like_count = SiteSetting(key='blogger_likes', value='0')
        db.session.add(like_count)
    like_count.value = str(int(like_count.value) + 1)
    db.session.commit()
    return jsonify({'likes': int(like_count.value)})

@app.route('/api/gallery', methods=['GET'])
def get_gallery():
    images = Gallery.query.order_by(Gallery.created_at.desc()).all()
    return jsonify([{
        'id': g.id,
        'title': g.title,
        'image_path': g.image_path,
        'description': g.description,
        'created_at': g.created_at.isoformat()
    } for g in images])

@app.route('/api/gallery', methods=['POST'])
@jwt_required()
def add_gallery():
    title = request.form.get('title', '')
    description = request.form.get('description', '')
    
    if 'image' not in request.files:
        return jsonify({'error': 'No image file'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']:
        try:
            # 使用OSS存储
            if Config.USE_CLOUD_STORAGE:
                image_url = get_oss_storage().upload_file(file.stream, file.filename, 'gallery')
                if not image_url:
                    return jsonify({'error': 'OSS upload failed: Invalid OSS configuration or network error'}), 500
            else:
                # 本地存储（保持原有逻辑）
                filename = str(datetime.now().timestamp()).replace('.', '') + '_' + file.filename
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                image_url = f'/uploads/{filename}'
            
            gallery = Gallery(
                title=title,
                description=description,
                image_path=image_url
            )
            db.session.add(gallery)
            db.session.commit()
            return jsonify({'message': 'Image added'}), 201
        except Exception as e:
            return jsonify({'error': f'Upload failed: {str(e)}'}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/api/gallery/<int:id>', methods=['PUT'])
@jwt_required()
def update_gallery(id):
    gallery = Gallery.query.get_or_404(id)
    gallery.title = request.form.get('title', gallery.title)
    gallery.description = request.form.get('description', gallery.description)
    
    if 'image' in request.files:
        file = request.files['image']
        if file.filename != '' and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']:
            try:
                if Config.USE_CLOUD_STORAGE:
                    image_url = get_oss_storage().upload_file(file.stream, file.filename, 'gallery')
                    if image_url:
                        gallery.image_path = image_url
                else:
                    filename = str(datetime.now().timestamp()).replace('.', '') + '_' + file.filename
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    gallery.image_path = f'/uploads/{filename}'
            except Exception as e:
                return jsonify({'error': f'Upload failed: {str(e)}'}), 500
    
    db.session.commit()
    return jsonify({'message': 'Gallery updated'})

@app.route('/api/gallery/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_gallery(id):
    gallery = Gallery.query.get_or_404(id)
    db.session.delete(gallery)
    db.session.commit()
    return jsonify({'message': 'Image deleted'})

@app.route('/api/honors', methods=['GET'])
def get_honors():
    honors = Honor.query.order_by(Honor.date.desc()).all()
    return jsonify([{
        'id': h.id,
        'title': h.title,
        'description': h.description,
        'date': h.date.isoformat() if h.date else None,
        'image_path': h.image_path
    } for h in honors])

@app.route('/api/honors', methods=['POST'])
@jwt_required()
def add_honor():
    title = request.form.get('title', '')
    description = request.form.get('description', '')
    date_str = request.form.get('date')
    
    honor = Honor(
        title=title,
        description=description,
        date=datetime.fromisoformat(date_str) if date_str else None
    )
    
    if 'image' in request.files:
        file = request.files['image']
        if file.filename != '' and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']:
            try:
                if Config.USE_CLOUD_STORAGE:
                    image_url = get_oss_storage().upload_file(file.stream, file.filename, 'honors')
                else:
                    filename = str(datetime.now().timestamp()).replace('.', '') + '_' + file.filename
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    image_url = f'/uploads/{filename}'
                honor.image_path = image_url
            except Exception as e:
                return jsonify({'error': f'Upload failed: {str(e)}'}), 500
    
    db.session.add(honor)
    db.session.commit()
    return jsonify({'message': 'Honor added'}), 201

@app.route('/api/honors/<int:id>', methods=['PUT'])
@jwt_required()
def update_honor(id):
    honor = Honor.query.get_or_404(id)
    honor.title = request.form.get('title', honor.title)
    honor.description = request.form.get('description', honor.description)
    
    date_str = request.form.get('date')
    if date_str:
        honor.date = datetime.fromisoformat(date_str)
    
    if 'image' in request.files:
        file = request.files['image']
        if file.filename != '' and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']:
            try:
                if Config.USE_CLOUD_STORAGE:
                    image_url = get_oss_storage().upload_file(file.stream, file.filename, 'honors')
                else:
                    filename = str(datetime.now().timestamp()).replace('.', '') + '_' + file.filename
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    image_url = f'/uploads/{filename}'
                honor.image_path = image_url
            except Exception as e:
                return jsonify({'error': f'Upload failed: {str(e)}'}), 500
    
    db.session.commit()
    return jsonify({'message': 'Honor updated'})

@app.route('/api/honors/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_honor(id):
    honor = Honor.query.get_or_404(id)
    db.session.delete(honor)
    db.session.commit()
    return jsonify({'message': 'Honor deleted'})

@app.route('/api/mubu_notes', methods=['GET'])
def get_mubu_notes():
    notes = MubuNote.query.order_by(MubuNote.created_at.desc()).all()
    return jsonify([{
        'id': note.id,
        'title': note.title,
        'url': note.url,
        'description': note.description,
        'created_at': note.created_at.isoformat(),
        'updated_at': note.updated_at.isoformat()
    } for note in notes])

@app.route('/api/mubu_notes', methods=['POST'])
@jwt_required()
def add_mubu_note():
    data = request.get_json()
    note = MubuNote(
        title=data['title'],
        url=data['url'],
        description=data.get('description', '')
    )
    db.session.add(note)
    db.session.commit()
    return jsonify({'message': 'Note added'}), 201

@app.route('/api/mubu_notes/<int:id>', methods=['PUT'])
@jwt_required()
def update_mubu_note(id):
    note = MubuNote.query.get_or_404(id)
    data = request.get_json()
    note.title = data.get('title', note.title)
    note.url = data.get('url', note.url)
    note.description = data.get('description', note.description)
    db.session.commit()
    return jsonify({'message': 'Note updated'})

@app.route('/api/mubu_notes/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_mubu_note(id):
    note = MubuNote.query.get_or_404(id)
    db.session.delete(note)
    db.session.commit()
    return jsonify({'message': 'Note deleted'})

@app.route('/api/upload', methods=['POST'])
@jwt_required()
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']:
        try:
            if Config.USE_CLOUD_STORAGE:
                file_url = get_oss_storage().upload_file(file.stream, file.filename, 'uploads')
                return jsonify({'filename': file.filename, 'url': file_url}), 201
            else:
                filename = str(datetime.now().timestamp()).replace('.', '') + '_' + file.filename
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                return jsonify({'filename': filename, 'url': f'/uploads/{filename}'}), 201
        except Exception as e:
            return jsonify({'error': f'Upload failed: {str(e)}'}), 500
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/user', methods=['GET'])
@jwt_required()
def get_user():
    user_id = int(get_jwt_identity())
    user = User.query.get_or_404(user_id)
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'avatar': user.avatar,
        'bio': user.bio,
        'site_name': user.site_name,
        'site_description': user.site_description
    })

@app.route('/api/user', methods=['PUT'])
@jwt_required()
def update_user():
    data = request.get_json()
    user_id = int(get_jwt_identity())
    user = User.query.get_or_404(user_id)
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    user.avatar = data.get('avatar', user.avatar)
    user.bio = data.get('bio', user.bio)
    user.site_name = data.get('site_name', user.site_name)
    user.site_description = data.get('site_description', user.site_description)
    
    if data.get('password'):
        user.set_password(data['password'])
    
    db.session.commit()
    return jsonify({'message': 'User updated'})

@app.route('/api/settings', methods=['GET'])
def get_settings():
    settings = SiteSetting.query.all()
    return jsonify({s.key: s.value for s in settings})

@app.route('/api/settings', methods=['POST'])
@jwt_required()
def save_settings():
    data = request.get_json()
    for key, value in data.items():
        setting = SiteSetting.query.filter_by(key=key).first()
        if setting:
            setting.value = value
        else:
            setting = SiteSetting(key=key, value=value)
            db.session.add(setting)
    db.session.commit()
    return jsonify({'message': 'Settings saved'})

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
    if not user_message:
        return jsonify({'error': 'Message is required'}), 400

    api_key = os.environ.get('GLM_API_KEY')
    api_url = os.environ.get('GLM_API_URL', 'https://open.bigmodel.cn/api/paas/v4/chat/completions')

    if not api_key:
        return jsonify({'reply': 'GLM API Key 未配置，请在 .env 文件中设置 GLM_API_KEY。'})

    try:
        response = http_requests.post(
            api_url,
            headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'glm-4-flash',
                'messages': [
                    {
                        'role': 'system',
                        'content': '你是一名计算机科学与技术专业的女学生，MBTI为INTJ。回答风格应符合INTJ特质：理性高效、逻辑清晰、注重结果、直接坦率、善于分析和解决问题。只有当被明确问及"你是谁"或要求自我介绍时，才回答"我是ZHH"。日常对话中无需提及自己的名字。'
                    },
                    {
                        'role': 'user',
                        'content': user_message
                    }
                ],
                'temperature': 0.7,
                'max_tokens': 1024
            },
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            reply = result['choices'][0]['message']['content']
            return jsonify({'reply': reply})
        else:
            return jsonify({'reply': f'AI 服务暂时不可用（错误码：{response.status_code}），请稍后再试。'})
    except http_requests.exceptions.Timeout:
        return jsonify({'reply': 'AI 响应超时，请稍后再试。'})
    except Exception as e:
        return jsonify({'reply': f'AI 服务出现异常，请稍后再试。'})

# ============ Movie CRUD ============

@app.route('/api/movies', methods=['GET'])
def get_movies():
    movies = Movie.query.order_by(Movie.created_at.desc()).all()
    return jsonify([{
        'id': m.id,
        'title': m.title,
        'poster': m.poster,
        'director': m.director,
        'year': m.year,
        'genre': m.genre,
        'rating': m.rating,
        'review': m.review,
        'description': m.description,
        'created_at': m.created_at.isoformat()
    } for m in movies])

@app.route('/api/movies', methods=['POST'])
@jwt_required()
def add_movie():
    title = request.form.get('title', '')
    director = request.form.get('director', '')
    year = request.form.get('year', '')
    genre = request.form.get('genre', '')
    rating = request.form.get('rating', '')
    description = request.form.get('description', '')
    review = request.form.get('review', '')
    
    poster_path = ''
    if 'poster' in request.files:
        file = request.files['poster']
        if file.filename != '':
            ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
            if ext in {'png', 'jpg', 'jpeg', 'gif'}:
                try:
                    if Config.USE_CLOUD_STORAGE:
                        poster_path = get_oss_storage().upload_file(file.stream, file.filename, 'movies/posters')
                    else:
                        filename = str(datetime.now().timestamp()).replace('.', '') + '_poster_' + file.filename
                        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        file.save(filepath)
                        poster_path = f'/uploads/{filename}'
                except Exception as e:
                    return jsonify({'error': f'Upload failed: {str(e)}'}), 500
    
    movie = Movie(
        title=title,
        poster=poster_path,
        director=director if director else None,
        year=int(year) if year else None,
        genre=genre if genre else None,
        rating=float(rating) if rating else None,
        review=review if review else None,
        description=description if description else None
    )
    db.session.add(movie)
    db.session.commit()
    return jsonify({'message': 'Movie added', 'id': movie.id}), 201

@app.route('/api/movies/<int:id>', methods=['PUT'])
@jwt_required()
def update_movie(id):
    movie = Movie.query.get_or_404(id)
    movie.title = request.form.get('title', movie.title)
    movie.director = request.form.get('director', movie.director)
    
    year = request.form.get('year', '')
    movie.year = int(year) if year else movie.year
    
    movie.genre = request.form.get('genre', movie.genre)
    
    rating = request.form.get('rating', '')
    movie.rating = float(rating) if rating else movie.rating
    
    movie.description = request.form.get('description', movie.description)
    movie.review = request.form.get('review', movie.review)
    
    if 'poster' in request.files:
        file = request.files['poster']
        if file.filename != '':
            ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
            if ext in {'png', 'jpg', 'jpeg', 'gif'}:
                try:
                    if Config.USE_CLOUD_STORAGE:
                        poster_url = get_oss_storage().upload_file(file.stream, file.filename, 'movies/posters')
                        if poster_url:
                            movie.poster = poster_url
                    else:
                        filename = str(datetime.now().timestamp()).replace('.', '') + '_poster_' + file.filename
                        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        file.save(filepath)
                        movie.poster = f'/uploads/{filename}'
                except Exception as e:
                    return jsonify({'error': f'Poster upload failed: {str(e)}'}), 500
    
    db.session.commit()
    return jsonify({'message': 'Movie updated'})

@app.route('/api/movies/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_movie(id):
    movie = Movie.query.get_or_404(id)
    db.session.delete(movie)
    db.session.commit()
    return jsonify({'message': 'Movie deleted'})

# ============ Music CRUD ============

@app.route('/api/music', methods=['GET'])
def get_music():
    songs = Music.query.order_by(Music.created_at.desc()).all()
    return jsonify([{
        'id': s.id,
        'title': s.title,
        'artist': s.artist,
        'album': s.album,
        'cover_path': s.cover_path,
        'file_path': s.file_path,
        'genre': s.genre,
        'description': s.description,
        'created_at': s.created_at.isoformat()
    } for s in songs])

@app.route('/api/music', methods=['POST'])
@jwt_required()
def add_music():
    title = request.form.get('title', '')
    artist = request.form.get('artist', '')
    album = request.form.get('album', '')
    genre = request.form.get('genre', '')
    description = request.form.get('description', '')
    
    if 'file' not in request.files:
        return jsonify({'error': 'No music file'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
    if ext not in {'mp3', 'wav', 'flac', 'aac'}:
        return jsonify({'error': 'Invalid audio format'}), 400
    
    try:
        if Config.USE_CLOUD_STORAGE:
            file_url = get_oss_storage().upload_file(file.stream, file.filename, 'music')
        else:
            filename = str(datetime.now().timestamp()).replace('.', '') + '_' + file.filename
            filepath = os.path.join(app.config['MUSIC_FOLDER'], filename)
            file.save(filepath)
            file_url = f'/music_uploads/{filename}'
    except Exception as e:
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500
    
    cover_path = ''
    if 'cover' in request.files:
        cover_file = request.files['cover']
        if cover_file.filename != '':
            cover_ext = cover_file.filename.rsplit('.', 1)[1].lower() if '.' in cover_file.filename else ''
            if cover_ext in {'png', 'jpg', 'jpeg', 'gif'}:
                try:
                    if Config.USE_CLOUD_STORAGE:
                        cover_path = get_oss_storage().upload_file(cover_file.stream, cover_file.filename, 'music/covers')
                    else:
                        cover_filename = str(datetime.now().timestamp()).replace('.', '') + '_cover_' + cover_file.filename
                        cover_filepath = os.path.join(app.config['UPLOAD_FOLDER'], cover_filename)
                        cover_file.save(cover_filepath)
                        cover_path = f'/uploads/{cover_filename}'
                except Exception as e:
                    return jsonify({'error': f'Cover upload failed: {str(e)}'}), 500
    
    music = Music(
        title=title,
        artist=artist,
        album=album,
        genre=genre,
        description=description,
        cover_path=cover_path,
        file_path=file_url
    )
    db.session.add(music)
    db.session.commit()
    return jsonify({'message': 'Music added', 'id': music.id}), 201

@app.route('/api/music/<int:id>', methods=['PUT'])
@jwt_required()
def update_music(id):
    music = Music.query.get_or_404(id)
    music.title = request.form.get('title', music.title)
    music.artist = request.form.get('artist', music.artist)
    music.album = request.form.get('album', music.album)
    music.genre = request.form.get('genre', music.genre)
    music.description = request.form.get('description', music.description)
    
    if 'file' in request.files:
        file = request.files['file']
        if file.filename != '':
            ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
            if ext in {'mp3', 'wav', 'flac', 'aac'}:
                try:
                    if Config.USE_CLOUD_STORAGE:
                        file_url = get_oss_storage().upload_file(file.stream, file.filename, 'music')
                        if file_url:
                            music.file_path = file_url
                    else:
                        filename = str(datetime.now().timestamp()).replace('.', '') + '_' + file.filename
                        filepath = os.path.join(app.config['MUSIC_FOLDER'], filename)
                        file.save(filepath)
                        music.file_path = f'/music_uploads/{filename}'
                except Exception as e:
                    return jsonify({'error': f'File upload failed: {str(e)}'}), 500
    
    if 'cover' in request.files:
        cover_file = request.files['cover']
        if cover_file.filename != '':
            cover_ext = cover_file.filename.rsplit('.', 1)[1].lower() if '.' in cover_file.filename else ''
            if cover_ext in {'png', 'jpg', 'jpeg', 'gif'}:
                try:
                    if Config.USE_CLOUD_STORAGE:
                        cover_url = get_oss_storage().upload_file(cover_file.stream, cover_file.filename, 'music/covers')
                        if cover_url:
                            music.cover_path = cover_url
                    else:
                        cover_filename = str(datetime.now().timestamp()).replace('.', '') + '_cover_' + cover_file.filename
                        cover_filepath = os.path.join(app.config['UPLOAD_FOLDER'], cover_filename)
                        cover_file.save(cover_filepath)
                        music.cover_path = f'/uploads/{cover_filename}'
                except Exception as e:
                    return jsonify({'error': f'Cover upload failed: {str(e)}'}), 500
    
    db.session.commit()
    return jsonify({'message': 'Music updated'})

@app.route('/api/music/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_music(id):
    music = Music.query.get_or_404(id)
    db.session.delete(music)
    db.session.commit()
    return jsonify({'message': 'Music deleted'})

@app.route('/music_uploads/<filename>')
def music_file(filename):
    return send_from_directory(app.config['MUSIC_FOLDER'], filename)