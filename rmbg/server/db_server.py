from sqlalchemy import create_engine, Column, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import sessionmaker
from rmbg.config import get_config
#from fly_log import debug_print as print, log_time, set_log_to_file
#set_log_to_file("rmbg.log")
Base = declarative_base()


class TaskLock(Base):
  
    __tablename__ = get_config.read_yaml_file()["rmbg"]["work_setting"]["Seize_mode_lock_db"]["table"]

    picture_in_processing = Column(String, primary_key=True)
    storage_time = Column(DateTime, default=datetime.now())
    expiration_time = Column(DateTime, default=lambda: datetime.now() + timedelta(minutes=2))
    operation_device = Column(String)
    image_size = Column(Float)



# 5.21 更改
class MySQLTaskLocker:
    """用于内存锁相关的操作
    """    
    def __init__(self):
        host = get_config.read_yaml_file()["rmbg"]["work_setting"]["Seize_mode_lock_db"]["host"]
        user = get_config.read_yaml_file()["rmbg"]["work_setting"]["Seize_mode_lock_db"]["user"]
        password = get_config.read_yaml_file()["rmbg"]["work_setting"]["Seize_mode_lock_db"]["password"]
        database = get_config.read_yaml_file()["rmbg"]["work_setting"]["Seize_mode_lock_db"]["database"]
        self.engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{database}")
        self.Session = sessionmaker(bind=self.engine)


    def insert_data(self, task_lock):
        """向数据库中写数据

        Args:
            task_lock (TaskLock): 正在被操作的图片的相关信息
        """        
        session = self.Session()
        # task_lock = TaskLock(picture_in_processing=picture_in_processing)
        try:
            session.add(task_lock)
            session.commit()
            #print("Data inserted successfully.")
        except Exception as e:
            print(f"Error1: {e}")
            session.rollback()
        finally:
            session.close()


    def delete_data(self, picture_in_processing):
        session = self.Session()
        try:
            task_lock = session.query(TaskLock).filter_by(picture_in_processing=picture_in_processing).first()
            if task_lock:
                session.delete(task_lock)
                session.commit()
                #print("Data deleted successfully.")
            else:
                print("No matching record found.")
        except Exception as e:
            print(f"Error: {e}")
            session.rollback()
        finally:
            session.close()


    def get_all(self):
        """获取所有的值

        Returns:
            _type_: _description_
        """        
        session = self.Session()
        try:
            # 查询所有正在处理的图片
            processing_pictures = session.query(TaskLock).all()
            
            return processing_pictures
        except Exception as e:
            # 处理异常
            print(f"Error occurred: {e}")
            return None
        finally:
            session.close()


    def is_value_in_database(self, value_to_check):
        """检查某个值是否存在，用来判断该图片是否

        Args:
            value_to_check (str): 待检测的图片名

        Returns:
            bool: 如果找到value_to_check，返回True；否则返回False
        """        
        session = self.Session()
        try:
            # 查询数据库中是否存在指定值
            self.timeout_self_deleting()
            result = session.query(TaskLock).filter(TaskLock.picture_in_processing == value_to_check).first()
            if result:
                return True
            else:
                return False
        except Exception as e:
            # 处理异常
            print(f"Error occurred: {e}")
            return False
        finally:
            session.close()
    

    def timeout_self_deleting(self):
        """检查过期时间并删除过期记录
        """
        session = self.Session()
        try:
            # 获取所有过期的记录
            expired_records = session.query(TaskLock).filter(TaskLock.expiration_time < datetime.now()).all()
            print("过期：", expired_records)
            
            # 删除过期记录
            for record in expired_records:
                session.delete(record)
                
            session.commit()
        except Exception as e:
            print(f"Error: {e}")
            session.rollback()
        finally:
            session.close()        