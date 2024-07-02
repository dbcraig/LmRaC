import json
import os
import pandas as pd


# User-defined Functions
class DEGbasic:
    """
    Perform initialization for DEGbasic.
    """
    def __init__(self):
        self.experimentsRoot = '/app/user/experiments/'                     # this is the Docker path to the experiments directory
        self.PathwayGenes ={}                                               # Dictionary of genes in each pathway
        self.GenePathways = {}                                              # Dictionary of pathways for each gene
        df = pd.read_csv('/app/data/KEGGhsaPathwayGenes.tsv', sep='\t')     # load DEGbasic data (part of the Docker image)
        for index, row in df.iterrows():
            pathway = row['keggID']
            gene = row['symbol']
            if pathway in self.PathwayGenes:
                self.PathwayGenes[pathway].append(gene)
            else:
                self.PathwayGenes[pathway] = [gene]
            if gene in self.GenePathways:
                self.GenePathways[gene].append(pathway)
            else:
                self.GenePathways[gene] = [pathway]
        pass

    # REQUIRED RESTserver.py FUNCTION to return a dictionary of availalbe user-functions for the REST interface
    def functionsList(self):
        """
        Functions are called by name in the REST interface.
        This maps the function names to the actual functions.
        """
        return {
            'initializeDEGbasic' : self.initializeDEGbasic,
            'getGeneExpression': self.getGeneExpression,
            'getTopExpressionResults': self.getTopExpressionResults,
            'getTopSignificantPathways': self.getTopSignificantPathways,
            'getPathwayGenes': self.getPathwayGenes,
            'getGenePathways': self.getGenePathways
        }
    

    # BEGIN USER-DEFINED FUNCTIONS
    def initializeDEGbasic(self):
        return "DEGbasic initialized."


    # 
    def getGeneExpression(self, params=None):
        """
        Get the gene expression data for a list of genes in an experiment.
        Default filename is 'DEG.tsv'.
        """
        params = json.loads(params)
        print(json.dumps(params, indent=4))
        geneList = [g['gene'] for g in params['geneArray']]
        experiment = params['experiment']
        if ( 'filename' in params ):
            filename = params['filename']
        else:
            filename = 'DEG.tsv'
        filepath = self.experimentsRoot + experiment + '/' + filename
        if ( os.path.exists(filepath) ):
            df = pd.read_csv(filepath, sep='\t')
            gene_df = pd.DataFrame(geneList, columns=['symbol'])
            result = pd.merge(gene_df, df, on='symbol', how='left')
            # if we don't find the gene in the DEG file, we'll return 'no data' for logfc and adjpv
            # otherwise the LLM will keep retrying to get the data
            result[['logfc', 'adjpv']] = result[['logfc', 'adjpv']].fillna('no data')
            result = result.to_json(orient='records')
            print(result)
            return {"experiment":experiment, "expression": result}  # return experiment for context
        else:
            return f"Function Error lmrac_getGeneExpression  Unable to find '{experiment}/{filename}'."  


    def getTopExpressionResults(self, params=None):
        """
        Get the top k differentially expressed genes from an experiment.
        Default filename is 'DEG.tsv'.
        """
        params = json.loads(params)
        print(json.dumps(params, indent=4))
        top_k = params['topK']
        byFoldChange = params['byFoldChange']
        experiment = params['experiment']
        if ( 'filename' in params ):
            filename = params['filename']
        else:
            filename = 'DEG.tsv'
        filepath = self.experimentsRoot + experiment + '/' + filename
        if ( os.path.exists(filepath) ):
            df = pd.read_csv(filepath, sep='\t')
            if ( byFoldChange ):
                df['absFoldChange'] = df['logfc'].abs()  # Create a new column for the absolute value of foldChange
                df = df.sort_values(by=['absFoldChange'], ascending=False)
            else:
                df = df.sort_values(by=['adjpv'], ascending=True)
            result = df[['symbol', 'logfc', 'adjpv']].head(top_k)  # Only include 'symbol', 'logfc', and 'adjpv' in the result
            result = result.to_json(orient='records')
            print(result)
            return {"experiment":experiment, "expression": result}  # return experiment for context
        else:
            return f"Function Error lmrac_getTopExpressionResults  Unable to find '{experiment}/{filename}'."  


    def getTopSignificantPathways(self, params=None):
        """
        Get the top k significant pathways from an experiment.
        Default filename is 'pathwaySig.tsv'.
        """
        params = json.loads(params)
        print(json.dumps(params, indent=4))
        top_k = params['topK']
        experiment = params['experiment']
        if ( 'filename' in params ):
            filename = params['filename']
        else:
            filename = 'pathwaySig.csv'
        filepath = self.experimentsRoot + experiment + '/' + filename
        if ( os.path.exists(filepath) ):
            df = pd.read_csv(filepath, sep=',')
            df = df.sort_values(by=['pv_fdr'], ascending=True)
            result = df[['pName','countDE','countAll','pv_fdr']].head(top_k)  # Only include 'pName', 'countDE', 'countAll', and 'pv_fdr' in the result
            result = result.to_json(orient='records')
            print(result)
            return {"experiment":experiment, "pathways": result}  # return experiment for context
        else:
            return f"Function Error getTopSignificantPathways  Unable to find '{experiment}/{filename}'." 


    def getPathwayGenes(self, params=None):
        """
        Get the genes in a given KEGG pathway.
        """
        params = json.loads(params)
        print(json.dumps(params, indent=4))
        pathwayID = params['pathwayID']
        if ( pathwayID in self.PathwayGenes ):
            return self.PathwayGenes[pathwayID]
        else:
            return []


    def getGenePathways(self, params=None):
        """
        Get the KEGG pathways for a given gene.
        """
        params = json.loads(params)
        print(json.dumps(params, indent=4))
        gene = params['gene']
        if ( gene in self.GenePathways ):
            return self.GenePathways[gene]
        else:
            return []
        


