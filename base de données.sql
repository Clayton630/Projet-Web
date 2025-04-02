#------------------------------------------------------------
#        Script MySQL.
#------------------------------------------------------------


#------------------------------------------------------------
# Table: Utilisateurs
#------------------------------------------------------------

CREATE TABLE Utilisateurs(
        id_user      Int NOT NULL ,
        mot_de_passe Varchar (50) NOT NULL ,
        nom          Varchar (50) NOT NULL ,
        email        Varchar (50) NOT NULL ,
        isadmin      Bool NOT NULL
	,CONSTRAINT Utilisateurs_PK PRIMARY KEY (id_user)
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: Categories
#------------------------------------------------------------

CREATE TABLE Categories(
        id_cat Int NOT NULL ,
        nom    Varchar (50) NOT NULL
	,CONSTRAINT Categories_PK PRIMARY KEY (id_cat)
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: Etablissments
#------------------------------------------------------------

CREATE TABLE Etablissments(
        id_etab      Int NOT NULL ,
        nom          Varchar (50) NOT NULL ,
        adrresse     Varchar (50) NOT NULL ,
        lattitude    Float (10.8) ,
        longitude    Float (10.8) ,
        id_cat       Int NOT NULL
	,CONSTRAINT Etablissments_PK PRIMARY KEY (id_etab)

	,CONSTRAINT Etablissments_Categories_FK FOREIGN KEY (id_cat) REFERENCES Categories(id_cat)
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: Retours
#------------------------------------------------------------

CREATE TABLE Retours(
        id_retour       Varchar NOT NULL ,
        note            Int NOT NULL ,
        commentaire     Varchar (150) NOT NULL ,
        date            Date NOT NULL ,
        id_user         Int NOT NULL ,
        id_etab         Int NOT NULL
	,CONSTRAINT Retours_PK PRIMARY KEY (id_retour)

	,CONSTRAINT Retours_Utilisateurs_FK FOREIGN KEY (id_user) REFERENCES Utilisateurs(id_user)
	,CONSTRAINT Retours_Etablissments0_FK FOREIGN KEY (id_etab) REFERENCES Etablissments(id_etab)
)ENGINE=InnoDB;


