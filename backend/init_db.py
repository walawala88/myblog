from app import app, db
from models import User, Category, Tag, Post, Comment, Gallery, Honor, SiteSetting, Movie, Music
from datetime import datetime

with app.app_context():
    db.create_all()

    # ========== 1. 初始化管理员用户 ==========
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin',
            email='admin@example.com',
            bio='博客管理员',
            site_name='个人博客',
            site_description='一个分享技术与生活的个人博客'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        print('[INIT] 管理员账号已创建: admin / admin123')

    # ========== 2. 初始化文章分类 ==========
    default_categories = [
        {'name': '技术分享', 'slug': 'tech-share', 'desc': '编程技术、框架使用等分享'},
        {'name': '生活随笔', 'slug': 'life-essay', 'desc': '日常生活中的感悟与记录'},
        {'name': '读书笔记', 'slug': 'reading-notes', 'desc': '读书心得与好文摘录'},
        {'name': '工作经验', 'slug': 'work-experience', 'desc': '工作中的经验总结与思考'},
    ]
    for cat in default_categories:
        if not Category.query.filter_by(name=cat['name']).first():
            c = Category(name=cat['name'], slug=cat['slug'], description=cat['desc'])
            db.session.add(c)
            print(f'[INIT] 分类已创建: {cat["name"]}')

    # ========== 3. 初始化电影数据（海报使用 OSS 路径格式） ==========
    from config import Config

    oss_base = Config.OSS_BASE_URL if Config.USE_CLOUD_STORAGE else '/uploads'

    sample_movies = [
        {
            'title': '肖申克的救赎', 'director': '弗兰克·德拉邦特', 'year': 1994,
            'genre': '剧情', 'rating': 9.7,
            'description': '希望是美好的，也许是人间至善，而美好的事物永不消逝。一位银行家被冤入狱后，用20年时间完成自我救赎的故事。',
            'review': '影史最伟大的作品之一，关于希望与自由的永恒赞歌。蒂姆·罗宾斯和摩根·弗里曼的表演堪称完美。',
            'poster': f'{oss_base}/movies/posters/shawshank.jpg' if oss_base else ''
        },
        {
            'title': '盗梦空间', 'director': '克里斯托弗·诺兰', 'year': 2010,
            'genre': '科幻', 'rating': 9.3,
            'description': '多姆·柯布是一位经验老道的窃贼，他能潜入人们梦境中盗取潜意识中的秘密。',
            'review': '诺兰用非线性叙事构建了一个多重梦境世界，视觉奇观与哲学思辨完美融合。',
            'poster': f'{oss_base}/movies/posters/inception.jpg' if oss_base else ''
        },
        {
            'title': '星际穿越', 'director': '克里斯托弗·诺兰', 'year': 2014,
            'genre': '科幻', 'rating': 9.4,
            'description': '一群探险者穿越虫洞，为人类寻找新家园的壮丽旅程。在时间与空间的维度中，爱是唯一能穿越维度的力量。',
            'review': '硬科幻外壳下的温情内核，汉斯·季默的配乐让整部电影升华到了另一个高度。',
            'poster': f'{oss_base}/movies/posters/interstellar.jpg' if oss_base else ''
        },
        {
            'title': '千与千寻', 'director': '宫崎骏', 'year': 2001,
            'genre': '动漫', 'rating': 9.4,
            'description': '少女千寻意外来到神灵世界，为了救变成猪的父母，她在汤屋中工作，经历了一段奇幻的成长之旅。',
            'review': '宫崎骏的巅峰之作，每一个画面都是艺术品，故事温暖又深刻。',
            'poster': f'{oss_base}/movies/posters/spirited_away.jpg' if oss_base else ''
        },
        {
            'title': '楚门的世界', 'director': '彼得·威尔', 'year': 1998,
            'genre': '剧情', 'rating': 9.3,
            'description': '楚门从出生起就生活在一个巨大的摄影棚中，他的一切都是被安排好的真人秀节目。',
            'review': '对媒体操控和个人自由的深刻反思，金·凯瑞用喜剧演绎了一个悲剧内核的故事。',
            'poster': f'{oss_base}/movies/posters/truman_show.jpg' if oss_base else ''
        },
        {
            'title': '功夫', 'director': '周星驰', 'year': 2004,
            'genre': '喜剧', 'rating': 8.7,
            'description': '小混混阿星误闯猪笼城寨，意外卷入了斧头帮与隐居高手之间的对决。',
            'review': '周星驰的集大成之作，将功夫与喜剧完美结合，每个角色都令人难忘。',
            'poster': f'{oss_base}/movies/posters/kungfu_hustle.jpg' if oss_base else ''
        },
        {
            'title': '泰坦尼克号', 'director': '詹姆斯·卡梅隆', 'year': 1997,
            'genre': '爱情', 'rating': 9.4,
            'description': '穷画家杰克和贵族少女露丝在泰坦尼克号上坠入爱河，然而巨轮撞上冰山...',
            'review': '史诗级爱情灾难片，莱昂纳多和凯特的化学反应震撼了整个世界。',
            'poster': f'{oss_base}/movies/posters/titanic.jpg' if oss_base else ''
        },
        {
            'title': '禁闭岛', 'director': '马丁·斯科塞斯', 'year': 2010,
            'genre': '悬疑', 'rating': 8.8,
            'description': '联邦警官泰迪来到禁闭岛调查一桩离奇失踪案，却发现岛上隐藏着更深的秘密。',
            'review': '一层层剥开的心理悬疑，结局让人脊背发凉，莱昂纳多的表演入木三分。',
            'poster': f'{oss_base}/movies/posters/shutter_island.jpg' if oss_base else ''
        },
        {
            'title': '大话西游之大圣娶亲', 'director': '刘镇伟', 'year': 1995,
            'genre': '喜剧', 'rating': 9.2,
            'description': '至尊宝回到五百年前，遇到了给他三颗痣的紫霞仙子，一段跨越时空的爱恋就此展开。',
            'review': '初看是喜剧，再看是悲剧，最后发现是人生。周星驰最被低估的神作。',
            'poster': f'{oss_base}/movies/posters/chinese_odyssey.jpg' if oss_base else ''
        },
        {
            'title': '龙猫', 'director': '宫崎骏', 'year': 1988,
            'genre': '动漫', 'rating': 9.2,
            'description': '姐妹俩搬到乡间居住，遇到了只有纯真孩童才能看见的森林精灵——龙猫。',
            'review': '最纯粹的童真与美好，宫崎骏用最简单的故事打动了所有人的心。',
            'poster': f'{oss_base}/movies/posters/totoro.jpg' if oss_base else ''
        },
    ]

    for m in sample_movies:
        if not Movie.query.filter_by(title=m['title']).first():
            movie = Movie(
                title=m['title'],
                poster=m['poster'],
                director=m['director'],
                year=m['year'],
                genre=m['genre'],
                rating=m['rating'],
                description=m['description'],
                review=m['review']
            )
            db.session.add(movie)
            print(f'[INIT] 电影已添加: {m["title"]}')

    # ========== 4. 初始化站点设置 ==========
    default_settings = {
        'blogger_likes': '0',
        'site_title': '个人博客',
        'site_subtitle': '分享技术与生活',
        'about_me': '热爱编程、电影与音乐，用博客记录生活与技术成长。',
    }
    for key, value in default_settings.items():
        if not SiteSetting.query.filter_by(key=key).first():
            setting = SiteSetting(key=key, value=value)
            db.session.add(setting)
            print(f'[INIT] 设置已创建: {key}')

    db.session.commit()
    print('\n========================================')
    print('  数据库初始化完成！')
    print('  管理员账号: admin / admin123')
    print(f'  已添加 {len(sample_movies)} 部电影')
    print(f'  OSS 存储状态: {"已启用" if Config.USE_CLOUD_STORAGE else "未启用（本地存储）"}')
    if Config.USE_CLOUD_STORAGE:
        print(f'  OSS 域名: {Config.OSS_BASE_URL}')
    print('========================================\n')