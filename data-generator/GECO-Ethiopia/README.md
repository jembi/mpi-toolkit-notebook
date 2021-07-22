Data Generator
=

To create the csv datasets:

1. ```conda activate rpy2```
2. ```source ./create-datasets.sh```

Data-generator in JupyterLab.

1. Prerequisites:

   a)  Install Miniconda3 (if not installed on your machine)
   
      Download the latest shell script
         ```wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.s```
      
      Make the miniconda installation script executable: 
         ```chmod +x Miniconda3-latest-Linux-x86_64.sh```
      
      Run miniconda installation script:
         ```./Miniconda3-latest-Linux-x86_64.sh```
      
   b)  Download MPI toolkit 
   
2. Install JupyterLab using:
   ```conda install -c conda-forge jupyterlab```
3. Open Jupyterlab using:
   ```jupyter-lab```

4. Open jupyter terminal

5. Create python 3.7 environment and run:
   
   a) ```conda create -n ‘name’ python=3.7``` 
   
   b) ```conda activate ‘name’```
   
   c) ```conda install pandas```
   
   d) ```conda install rpy2 -c conda-forge```
   
   e)  ```conda install wxpython -c conda-forge```
   
6. cd to source of create-datasets.sh 
7. run```./create-datasets.sh```
