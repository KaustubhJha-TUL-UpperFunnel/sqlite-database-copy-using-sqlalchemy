import sqlalchemy as sql
import sqlalchemy.orm as orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session,sessionmaker,aliased,relationship

Base = declarative_base()

class UserTable(Base):
    __tablename__ = 'user_table'
    user_id = sql.Column(sql.Integer , autoincrement  = True, primary_key = True )
    user_name = sql.Column(sql.String(40), unique = True, nullable = False)
    user_password = sql.Column(sql.String(40), nullable = False)

    User_Rides = orm.relationship("RideTable" , cascade = "all,delete")
    Ongoing_rides = orm.relationship("RideUsersTable" , cascade = "all,delete")
    
    def write_to_db(self):
        s.add(self)
        s.commit()
    
    def read_from_db(self):
        s.delete(self)
        s.commit()
    
    def delete_from_db(self):
        s.delete(self)
        s.commit()



class RideTable(Base):
    __tablename__ = 'ride_user_table'
    ride_id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    created_by = sql.Column(sql.String(80), sql.ForeignKey(
        "user_table.user_name"), nullable=False)
    source = sql.Column(sql.Integer, nullable=False)
    destination = sql.Column(sql.Integer, nullable=False)
    timestamp = sql.Column(sql.DateTime, nullable=False)
    ride_users = orm.relationship("RideUsersTable", cascade="all,delete")

    def write_to_db(self):
        s.add(self)
        s.commit()
        return self.ride_id

    def delete_from_db(self):
        s.delete(self)
        s.commit()

    


class RideUsersTable(Base):
    __tablename__ = 'ride_users_table'
    ride_users_id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    ride_table_id = sql.Column(sql.Integer, sql.ForeignKey("ride_user_table.ride_id"), nullable=False)
    user_table_name = sql.Column(sql.String(40), sql.ForeignKey(
        "user_table.user_name"), nullable=False)


    def write_to_db(self):
        s.add(self)
        s.commit()
        return self.ride_table_id

    def delete_from_db(self):
        s.delete(self)
        s.commit()



engine =  sql.create_engine("sqlite:///riders.db")
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
s = Session()


def copypdbDBtoRDB():

	engine_ =  sql.create_engine("sqlite:///pdb/riders.db")
	Base.metadata.create_all(bind=engine_)
	Session = sessionmaker(bind=engine_)
	s_ = Session()
	
	#copying UserTable
	queryS = s_.query(UserTable.user_id,UserTable.user_name,UserTable.user_password)
	#queryD = s.query(UserTable.user_id,UserTable.user_name,UserTable.user_password)
	
	queryS1 = s_.query(RideTable.ride_id,RideTable.created_by,RideTable.source,RideTable.destination,RideTable.timestamp)
	#queryD1 = s.query(RideTable.ride_id,RideTable.created_by,RideTable.source,RideTable.destination,RideTable.timestamp,RideTable.ride_users)
	
	queryS2 = s_.query(RideUsersTable.ride_users_id,RideUsersTable.ride_table_id,RideUsersTable.user_table_name)
	#queryD2 = s.query(RideUsersTable.ride_users_id,RideUsersTable.ride_table_id,RideUsersTable.user_table_name)
	
	#for row in queryS:
	num_rows_deleted = s.query(UserTable).delete()
	s.commit()
	num_rows_deleted = s.query(RideTable).delete()
	s.commit()
	num_rows_deleted = s.query(RideUsersTable).delete()
	s.commit()
	
	for row in queryS:
		user = UserTable()
		user.user_id = row[0]
		user.user_name = row[1]
		user.user_password = row[2]
		
		s.add(user)
		s.commit()
		
	for row in queryS1:
		ride = RideTable()
		ride.ride_id = row[0]
		ride.created_by = row[1]
		ride.source = row[2]
		ride.destination = row[3]
		ride.timestamp = row[4]
		
		s.add(ride)
		s.commit()
		
	for row in queryS2:
		userRide = RideUsersTable()
		userRide.ride_users_id = row[0]
		userRide.ride_table_id = row[1]
		userRide.user_table_name = row[2]
		
		s.add(userRide)
		s.commit()	        
	        
	s_.close()





copypdbDBtoRDB()