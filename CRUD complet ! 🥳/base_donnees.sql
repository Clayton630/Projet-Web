-- phpMyAdmin SQL Dump
-- version 4.2.7.1
-- http://www.phpmyadmin.net
--
-- Client :  localhost
-- Généré le :  Ven 25 Avril 2025 à 15:01
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Structure de la table `etablissments`
--

CREATE TABLE IF NOT EXISTS `etablissments` (
`id_etab` int(11) NOT NULL,
  `nom` varchar(50) NOT NULL,
  `adrresse` varchar(50) NOT NULL,
  `lattitude` float DEFAULT NULL,
  `longitude` float DEFAULT NULL,
  `id_cat` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci AUTO_INCREMENT=1 ;

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
  `mot_de_passe` varchar(50) NOT NULL,
  `nom` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `isadmin` tinyint(1) NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci AUTO_INCREMENT=4 ;

--
-- Contenu de la table `utilisateurs`
--

INSERT INTO `utilisateurs` (`id_user`, `mot_de_passe`, `nom`, `email`, `isadmin`) VALUES
(1, 'Clayton83', 'Clayton', 'claytonelhorga@icloud.com', 1),
(2, 'root', 'Utilisateur2', 'utilisateur2@gmail.com', 0),
(3, 'Clayton83', 'Clayton', 'claytonelhorga@icloud.com', 1);

--
-- Index pour les tables exportées
--

--
-- Index pour la table `categories`
--
ALTER TABLE `categories`
 ADD PRIMARY KEY (`id_cat`);

--
-- Index pour la table `etablissments`
--
ALTER TABLE `etablissments`
 ADD PRIMARY KEY (`id_etab`), ADD KEY `Etablissments_Categories_FK` (`id_cat`);

--
-- Index pour la table `retours`
--
ALTER TABLE `retours`
 ADD PRIMARY KEY (`id_retour`), ADD KEY `Retours_Utilisateurs_FK` (`id_user`), ADD KEY `Retours_Etablissments0_FK` (`id_etab`);

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
MODIFY `id_cat` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT pour la table `etablissments`
--
ALTER TABLE `etablissments`
MODIFY `id_etab` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT pour la table `utilisateurs`
--
ALTER TABLE `utilisateurs`
MODIFY `id_user` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=4;
--
-- Contraintes pour les tables exportées
--

--
-- Contraintes pour la table `etablissments`
--
ALTER TABLE `etablissments`
ADD CONSTRAINT `Etablissments_Categories_FK` FOREIGN KEY (`id_cat`) REFERENCES `categories` (`id_cat`);

--
-- Contraintes pour la table `retours`
--
ALTER TABLE `retours`
ADD CONSTRAINT `Retours_Etablissments0_FK` FOREIGN KEY (`id_etab`) REFERENCES `etablissments` (`id_etab`),
ADD CONSTRAINT `Retours_Utilisateurs_FK` FOREIGN KEY (`id_user`) REFERENCES `utilisateurs` (`id_user`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
