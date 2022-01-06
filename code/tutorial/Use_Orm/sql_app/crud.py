# CRUD 来自：创建、读取、更新和删除。
# Create, Read, Update, and Delete.

# 在这个文件中，我们将有可重用的函数来与数据库中的数据进行交互

from sqlalchemy.orm import Session

from . import models, schemas

# 读取单个用户
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# 由 Email 查找用户
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# 读取多个用户
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

# 创建用户
def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"

    # 创建实例
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)     # 添加实例到数据库会话
    db.commit()         # 将更改提交到数据
    db.refresh(db_user) # 刷新实例，以便获取其 ID
    return db_user

# 获取全部 Item
def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

# 创建用户与 Item 的绑定
def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item