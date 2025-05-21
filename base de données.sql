-- phpMyAdmin SQL Dump
-- version 4.2.7.1
-- http://www.phpmyadmin.net
--
-- Client :  localhost
-- Généré le :  Mar 13 Mai 2025 à 13:47
-- Version du serveur :  11.3.2-MariaDB
-- Version de PHP :  5.4.31

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Base de données :  `retoursdb`
--

-- --------------------------------------------------------

--
-- Structure de la table `categories`
--

CREATE TABLE IF NOT EXISTS `categories` (
`id_cat` int(11) NOT NULL,
  `nom` varchar(50) NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci AUTO_INCREMENT=2 ;

--
-- Contenu de la table `categories`
--

INSERT INTO `categories` (`id_cat`, `nom`) VALUES
(1, 'écoles');

-- --------------------------------------------------------

--
-- Structure de la table `etablissements`
--

CREATE TABLE IF NOT EXISTS `etablissements` (
`id_etab` int(11) NOT NULL,
  `nom` varchar(50) NOT NULL,
  `adresse` varchar(250) NOT NULL,
  `latitude` float DEFAULT NULL,
  `longitude` float DEFAULT NULL,
  `id_cat` int(11) NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci AUTO_INCREMENT=11 ;

--
-- Contenu de la table `etablissements`
--

INSERT INTO `etablissements` (`id_etab`, `nom`, `adresse`, `latitude`, `longitude`, `id_cat`) VALUES
(9, 'test accents', 'éé', 4, 5, 1),
(10, 'ISEN Toulon', 'Maison du numérique et de l''innovation, Pl. Georges Pompidou, 83000 Toulon', 47.6194, 6.1529, 1);

-- --------------------------------------------------------

--
-- Structure de la table `retours`
--

CREATE TABLE IF NOT EXISTS `retours` (
  `id_retour` varchar(50) NOT NULL,
  `note` int(11) NOT NULL,
  `commentaire` varchar(150) NOT NULL,
  `date` date NOT NULL,
  `id_user` int(11) NOT NULL,
  `id_etab` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `utilisateurs`
--

CREATE TABLE IF NOT EXISTS `utilisateurs` (
`id_user` int(11) NOT NULL,
  `mot_de_passe` varchar(256) DEFAULT NULL,
  `nom` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `isadmin` tinyint(1) NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci AUTO_INCREMENT=8 ;

--
-- Contenu de la table `utilisateurs`
--

INSERT INTO `utilisateurs` (`id_user`, `mot_de_passe`, `nom`, `email`, `isadmin`) VALUES
(6, 'scrypt:32768:8:1$gZ7YPZKo53Rse8Db$8e2154b2fd8db9d86b0cd7f4916df9b0f5b4a9cab7982df61e84b0ffeac49f77a0a80f4023fe4e3b1ba7dc66e244a89a6d157acd4fcfb22f8fbaa068b6530dff', 'clayton2', 'clayton2@gmail.com', 0),
(7, 'scrypt:32768:8:1$2Em18DeABiFcFVb7$bd1fc402b4df227e6cdbad72b649dc99b8ac1485c52cc62413ed46920730b601307916c13765edb938009788586880b1a6138d817af6f9e820af862077e3c125', 'Clayton', 'clayton.elhorga@isen.yncrea.fr', 1);

--
-- Index pour les tables exportées
--

--
-- Index pour la table `categories`
--
ALTER TABLE `categories`
 ADD PRIMARY KEY (`id_cat`);

--
-- Index pour la table `etablissements`
--
ALTER TABLE `etablissements`
 ADD PRIMARY KEY (`id_etab`), ADD KEY `Etablissements_Categories_FK` (`id_cat`);

--
-- Index pour la table `retours`
--
ALTER TABLE `retours`
 ADD PRIMARY KEY (`id_retour`), ADD KEY `Retours_Utilisateurs_FK` (`id_user`), ADD KEY `Retours_Etablissements0_FK` (`id_etab`);

--
-- Index pour la table `utilisateurs`
--
ALTER TABLE `utilisateurs`
 ADD PRIMARY KEY (`id_user`);

--
-- AUTO_INCREMENT pour les tables exportées
--

--
-- AUTO_INCREMENT pour la table `categories`
--
ALTER TABLE `categories`
MODIFY `id_cat` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT pour la table `etablissements`
--
ALTER TABLE `etablissements`
MODIFY `id_etab` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=11;
--
-- AUTO_INCREMENT pour la table `utilisateurs`
--
ALTER TABLE `utilisateurs`
MODIFY `id_user` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=8;
--
-- Contraintes pour les tables exportées
--

--
-- Contraintes pour la table `etablissements`
--
ALTER TABLE `etablissements`
ADD CONSTRAINT `Etablissements_Categories_FK` FOREIGN KEY (`id_cat`) REFERENCES `categories` (`id_cat`);

--
-- Contraintes pour la table `retours`
--
ALTER TABLE `retours`
ADD CONSTRAINT `Retours_Etablissements0_FK` FOREIGN KEY (`id_etab`) REFERENCES `etablissements` (`id_etab`),
ADD CONSTRAINT `Retours_Utilisateurs_FK` FOREIGN KEY (`id_user`) REFERENCES `utilisateurs` (`id_user`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
