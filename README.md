# APPSherbrooke

Projet pour automatiser une analyse multicritère selon les poids ajouter et selon les roulements voulus

# Conda 
il faut le fichier Requirements.txt pour avoir le même environnement
    
```
conda create --name <env> --file requirements.txt
```
    
les packages les plus important :
python 3.7.9
gdal 2.3.3
osgeo
geospanda
numpy 1.19.2

# RoadMap 
- [x] Recherche
- [x] contruction des premier geoprocessing
- [x] Rasterize, Reclassify et raster_calculator
- [x] Fonctione du proximity et de la reprojection
- [x] Réalisation des premier masques de criteres
- [x] Réalisation des premièere matrice de facteurs
- [x] Réalisation du core au complet
- [ ] Gestion des erreurs
- [ ] Gestion des axes a partir du excel
- [ ] La phase 2 (site propice)
- [ ] Création du Docker
- [ ] Réalisation des prétraitement (dissolve, add filed)
- [ ] documentation pour environnement
- [ ] Optimisation

