-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : localhost:8889
-- Généré le : mer. 30 avr. 2025 à 15:34
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

-- --------------------------------------------------------

--
-- Structure de la table `etablissments`
--

CREATE TABLE `etablissments` (
  `id_etab` int NOT NULL,
  `nom` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `adrresse` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `lattitude` float DEFAULT NULL,
  `longitude` float DEFAULT NULL,
  `id_cat` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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

-- --------------------------------------------------------

--
-- Structure de la table `Utilisateurs`
--

CREATE TABLE `Utilisateurs` (
  `id_user` int NOT NULL,
  `mot_de_passe` varchar(300) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `nom` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `isadmin` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `Utilisateurs`
--

INSERT INTO `Utilisateurs` (`id_user`, `mot_de_passe`, `nom`, `email`, `isadmin`) VALUES
(9, 'scrypt:32768:8:1$JX3pWO7qFV8efEr6$564ab332399a27f40285c3ac05a7862fceff187bbed5e0a46f5d6cfa7347b48171a3d75326e09f6d7e1b371d11359e9ece708868619a5337e92ee257c6a61f12', 'Clayton', 'claytonelhorga@icloud.com', 1),
(10, 'scrypt:32768:8:1$AmPJWYYSsA5QXBSq$41a9a21af4c565d1f6e4af531e07b818ec26512e49c134fc1b63730f88eb68ff5c10f514f0eea516497a02c9e26d2dc08a8f3b599dea048b9f9a888690f67c0a', 'Clayton2', 'clayton.elhorga@isen.yncrea.fr', 0);

--
-- Index pour les tables déchargées
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
  ADD PRIMARY KEY (`id_etab`),
  ADD KEY `Etablissments_Categories_FK` (`id_cat`);

--
-- Index pour la table `retours`
--
ALTER TABLE `retours`
  ADD PRIMARY KEY (`id_retour`),
  ADD KEY `Retours_Utilisateurs_FK` (`id_user`),
  ADD KEY `Retours_Etablissments0_FK` (`id_etab`);

--
-- Index pour la table `Utilisateurs`
--
ALTER TABLE `Utilisateurs`
  ADD PRIMARY KEY (`id_user`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `categories`
--
ALTER TABLE `categories`
  MODIFY `id_cat` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `etablissments`
--
ALTER TABLE `etablissments`
  MODIFY `id_etab` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `Utilisateurs`
--
ALTER TABLE `Utilisateurs`
  MODIFY `id_user` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Contraintes pour les tables déchargées
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
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
