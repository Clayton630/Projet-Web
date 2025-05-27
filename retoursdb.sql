-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : localhost:8889
-- Généré le : mar. 27 mai 2025 à 10:00
-- Version du serveur : 8.0.40
-- Version de PHP : 8.3.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `retoursdb`
--

-- --------------------------------------------------------

--
-- Structure de la table `categories`
--

CREATE TABLE `categories` (
  `id_cat` int NOT NULL,
  `nom` varchar(50) COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `categories`
--

INSERT INTO `categories` (`id_cat`, `nom`) VALUES
(1, 'écoles'),
(3, 'restaurant'),
(4, 'médical'),
(5, 'commerce');

-- --------------------------------------------------------

--
-- Structure de la table `etablissements`
--

CREATE TABLE `etablissements` (
  `id_etab` int NOT NULL,
  `nom` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `adresse` varchar(250) COLLATE utf8mb4_general_ci NOT NULL,
  `latitude` float DEFAULT NULL,
  `longitude` float DEFAULT NULL,
  `id_cat` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `etablissements`
--

INSERT INTO `etablissements` (`id_etab`, `nom`, `adresse`, `latitude`, `longitude`, `id_cat`) VALUES
(11, 'KFC Toulon Liberté', '14 place De La Liberté Toulon 83000 Toulon', 43.1257, 5.93126, 3),
(12, 'ISEN Toulon', 'Maison du numérique et de l\'innovation, Pl. Georges Pompidou, 83000 Toulon', 43.1207, 5.93903, 1),
(13, 'UFR Faculté de Droit', '35 Rue Alphonse Daudet, 83000 Toulon', 43.1214, 5.9382, 1),
(14, 'Hôpital Sainte Musse', '54 Rue Henri Sainte-Claire Deville, 83100', 43.1259, 5.9758, 4),
(15, 'Grande Pharmacie Lazare Carnot', '117 Avenue Lazare Carnot, 83000 Toulon', 43.1269, 5.92533, 4),
(16, 'Grande Pharmacie de Saint Jean', '282 Boulevard Léon Bourgeois, 83100 Toulon', 43.1208, 5.94862, 4),
(17, 'Galeries Lafayette Toulon', '9 Boulevard Strasbourg, 83000 Toulon', 43.1249, 5.93044, 5);

-- --------------------------------------------------------

--
-- Structure de la table `retours`
--

CREATE TABLE `retours` (
  `id_retour` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `note` int NOT NULL,
  `commentaire` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  `date` date NOT NULL,
  `id_user` int NOT NULL,
  `id_etab` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `retours`
--

INSERT INTO `retours` (`id_retour`, `note`, `commentaire`, `date`, `id_user`, `id_etab`) VALUES
('6-11-20250525000000', 2, 'A fuir, j\'ai eu la diarrhée (même si c\'était très bon)', '2025-05-25', 6, 11),
('7-11-20250525000000', 5, 'Super restaurant, j\'ai bien mangé !', '2025-05-25', 7, 11);

-- --------------------------------------------------------

--
-- Structure de la table `utilisateurs`
--

CREATE TABLE `utilisateurs` (
  `id_user` int NOT NULL,
  `mot_de_passe` varchar(256) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `nom` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `isadmin` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `utilisateurs`
--

INSERT INTO `utilisateurs` (`id_user`, `mot_de_passe`, `nom`, `email`, `isadmin`) VALUES
(6, 'scrypt:32768:8:1$gZ7YPZKo53Rse8Db$8e2154b2fd8db9d86b0cd7f4916df9b0f5b4a9cab7982df61e84b0ffeac49f77a0a80f4023fe4e3b1ba7dc66e244a89a6d157acd4fcfb22f8fbaa068b6530dff', 'clayton2', 'clayton2@gmail.com', 0),
(7, 'scrypt:32768:8:1$2Em18DeABiFcFVb7$bd1fc402b4df227e6cdbad72b649dc99b8ac1485c52cc62413ed46920730b601307916c13765edb938009788586880b1a6138d817af6f9e820af862077e3c125', 'Clayton', 'clayton.elhorga@isen.yncrea.fr', 1);

--
-- Index pour les tables déchargées
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
  ADD PRIMARY KEY (`id_etab`),
  ADD KEY `Etablissements_Categories_FK` (`id_cat`);

--
-- Index pour la table `retours`
--
ALTER TABLE `retours`
  ADD PRIMARY KEY (`id_retour`),
  ADD KEY `Retours_Utilisateurs_FK` (`id_user`),
  ADD KEY `Retours_Etablissements0_FK` (`id_etab`);

--
-- Index pour la table `utilisateurs`
--
ALTER TABLE `utilisateurs`
  ADD PRIMARY KEY (`id_user`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `categories`
--
ALTER TABLE `categories`
  MODIFY `id_cat` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT pour la table `etablissements`
--
ALTER TABLE `etablissements`
  MODIFY `id_etab` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT pour la table `utilisateurs`
--
ALTER TABLE `utilisateurs`
  MODIFY `id_user` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- Contraintes pour les tables déchargées
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
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
