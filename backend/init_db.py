from app import app, db
from models import User, Category, SiteSetting

with app.app_context():
    db.create_all()
    
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin',
            email='admin@example.com',
            site_name='我的博客',
            site_description='欢迎来到我的个人博客'
        )
        admin.set_password('admin123')
        db.session.add(admin)
    
    default_categories = ['技术分享', '生活随笔', '读书笔记', '工作经验']
    for name in default_categories:
        if not Category.query.filter_by(name=name).first():
            category = Category(
                name=name,
                slug=name.lower().replace(' ', '-'),
                description=f'{name}相关文章'
            )
            db.session.add(category)
    
    db.session.commit()
    print('Database initialized successfully!')