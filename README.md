![](img/LmRaC_3.png)

LmRaC (Language Model Research Assistant & Collaborator) is an LLM-based web application that enables users to explore, understand and interrogate their own biological experiments by:

-   incrementally building custom knowledge bases from the scientific literature, and

-   using custom functions to make quantitative data available to the language model.

LmRaC uses a multi-tier retrieval-augmented generation (RAG) design to index: domain knowledge, experimental context and experimental results. LmRaC is fully data-aware through the use of a user-defined REST API that allows the LLM to ask questions about data and results.

------------------------------------------------------------------------

## Table of Contents

> ### Getting Started
> 
> * [Prerequisites](#Prerequisites)
> * [Quick Start](#Quick-Start)
> * [Installation](#Installation)

> ### Application Windows & Configuration
> 
> * [LmRaC Homepage](#LmRaC-Homepage)
>   * [Commands](#Commands)
> * [Indexes Window](#Indexes-Window)
> * [Experiments Window](#Experiments-Window)
> * [Functions Window](#Functions-Window)
> * [Answers Window](#Answers-Window)
> * [Configuration](#Configuration)

> ### Usage, Workflow & Troubleshooting
> 
> * [Usage: Q & A](#Usage---Q-and-A)
> * [Usage: Experiments](#Usage---Experiments)
> * [Usage: User-Defined Functions](#Usage---User-Defined-Functions)
> * [Indexes and Experiments and Functions](#Indexes-and-Experiments-and-Functions)
> * [Troubleshooting](#Troubleshooting)

> ### Credits
> 
> * [How To Cite](#How-To-Cite)
> * [Contact](#Contact)

------------------------------------------------------------------------

## Prerequisites

### Docker

LmRaC runs as a web application in a Docker container. Users must therefore have either [Docker Engine](https://docs.docker.com/engine/install/) (CLI - Linux) or [Docker Desktop](https://docs.docker.com/desktop/install/linux-install/) (GUI - Linux, Mac, Windows) installed. If running Docker in the cloud, we recommend a container optimized OS. See [Installation](#Installation) below for details on installing Docker.

### OpenAI

LmRaC uses OpenAI's GPT-4o API to perform many language related functions. GPT does not per se answer user questions. Instead, it is used to assess the usefulness of primary source material for answering questions. Users of LmRaC must have an active OpenAI API account with an API key (see [OpenAI API keys](https://platform.openai.com/docs/quickstart)). Once a key has been created, it must be passed into the Docker container. This is typically done by creating an environment variable and then passing a reference to this variable in the **docker run** command using the **-e** option. 

```         
export OPENAI_API_KEY="sk-asdlfjlALJWEasdfLWERLWwwSFSSEwwwww"
```

When using Docker Desktop, keys are part of the container's Run settings (see [Container settings](#Container-settings)).

### Pinecone

[Pinecone](https://app.pinecone.io/) is a vector database used by LmRaC to store and search vector embedding of source material (i.e., indexes). Users must have an active Pinecone account then [create a Serverless API Key](https://docs.pinecone.io/guides/projects/understanding-projects#api-keys) from the Pinecone console. Once a key has been created, it must be passed into the Docker container. This is typically done by creating an environment variable and then passing a reference to this variable in the **docker run** command using the **-e** option.

```         
export PINECONE_API_KEY="2368ff63-8a81-43e3-9fd5-46e892b9d1b3"
```

When using Docker Desktop, keys are part of the container's Run settings (see [Container settings](#Container-settings)).

------------------------------------------------------------------------

## Quick Start

Pull the latest tagged image from Docker Hub. Run LmRaC using Docker Engine. If Docker is not installed or you're using Docker Desktop, see the [Installation](#Installation) instructions below. You'll need to pass API keys for OpenAI and Pinecone and mount your local directory (e.g., \$pwd) to the LmRaC */app/user* directory. The local directory is where user experiments are found and to where all LmRaC logs and output will be written.

```         
docker pull dbcraig/lmrac:latest
cd <your-lmrac-root>
docker run -m1024m -it -e OPENAI_API_KEY=${OPENAI_API_KEY} -e PINECONE_API_KEY=${PINECONE_API_KEY} -v $(pwd)/work:/app/user -v /etc/localtime:etc/localtime:ro -p 5000:5000 dbcraig/lmrac
```

Note, we recommend 1GB of memory and also mounting */etc/localtime* to insure container time is the same as server time.

Open LmRaC in your browser using *localhost*. For example, <http://localhost:5000> Typically, the port is 5000, but depending on your Docker configuration and what else is running on your host, this may be different (e.g., 55001 for Docker Desktop). The LmRaC homepage will open and LmRaC will initialize. Any problems (e.g., missing keys) will be reported.

![](img/LmRaC_init.png)

The first time you run LmRaC it will use a default configuration. See [Configuration](#Configuration) below for how to customize the configuration. When you quit LmRaC your current configuration is saved to *config/LmRaC.config* in the the mounted directory.

### Creating an Index

All questions are answered relative to an index of source material. So, set an index in Pinecone to store embeddings of the source articles. If the index does not exist, you'll be asked to create it. LmRaC will indicate how many paragraphs of information are currently stored in the index. Note that the command to set the index is in natural language, so you can ask something like: "Set index to test1" or "index = test1" or anything that indicates you want to set the index.

```         
[user]  set index to test1
[LmRaC] The current index has been set to 'test1'.
Index sizes are:
RAGdom : test1 (28810) 
RAGexp : test1-exp (123) 
```

Each index has two parts: 

- **RAGdom:** the general domain knowledge index for primary material (i.e., PubMed articles)
- **RAGexp:** the experiment specific index for secondary material (e.g., saved answers, protocols, background/context knowledge)

### Asking questions and populating your Index

Ask a question. LmRaC will analyze the question for any mention of genes, diseases or pathways using its vocabularies (see [Configuration](#Configuration)). It will summarize what it finds as the Search Context. If the index already contains information about any of these items, you will be given the option of updating the index (i.e., searching for more documents). If the index does not include information about one or more item in the question, it will initiate a search of PubMed and populate the index.

```
[user]  What is the difference between ESR1 and ESR2?
[LmRaC] How detailed an answer would you like (1-7)?
[user]  2
## Question
'What is the difference between ESR1 and ESR2?'
Answer complexity: 2
Analyzing question to determine genes, pathways and diseases...

## Search Context
Genes    : ['ESR1', 'ESR2']
Pathways :
Diseases :
## PubMed Search : Genes
### Gene ESR1
[LmRaC] 
Would you like to search PubMed for articles related to gene 'ESR1'? [y/N] 
[user]  yes

Number of citations for ESR1 = 4275
[LmRaC] How many citations would you like to download (up to top 100)?

[user]  10
Retrieving document metadata from PubMed
...
```

### Viewing Answers

Answers are displayed during processing and saved in the *sessions/finalAnswers/* directory along with information about the original query, generated sub-queries, references for the answer and a GPT4 assessment of the final answer.

To view the final answer (and its quality assessment) open the [Answers Window](#Answers-Window) by clicking on the Answers icon of the ([LmRaC Homepage](#LmRaC-Homepage)). From the Answers window answers can be viewed as markdown, HTML, downloaded, and/or saved to experiments as supplemental experiment documents.

### Quitting LmRaC

Exit LmRaC by typing "bye" or "exit" or "adios" in whatever language you prefer. You will be given the option to save your current configuration. The saved configuration includes your current index, experiment and any loaded functions. Once you quit the Docker container will exit.

### Next steps

Once you've asked some questions and received answers, you'll probably want to setup experiments into which you can save answers and upload quantitative results. You can then ask questions about your own experimental results! See 
[Experiments](#Usage---Experiments) and [Functions](#Usage---User-Defined-Functions) for more details.

------------------------------------------------------------------------

## Installation

LmRaC is a containerized web application. That means, everything you need to "install" and run LmRaC is packaged into a single Docker container. So, the only thing you need to install for any operating system is Docker. Once Docker is installed you simply "pull" the latest LmRaC release from [DockerHub](https://hub.docker.com/) and run it from Docker. That's it! No worrying about installing the correct version of Python or this or that library or confusing dependencies. It's all in the container!

If you're running on Linux then you have the option of installing the command-line version of Docker known as Docker Engine (aka Docker CE), otherwise you'll need to install Docker Desktop.

### Docker Engine (Linux)

#### Install Docker Engine

Installation instructions for Linux distros can be found at  [Install Docker Engine](https://docs.docker.com/engine/install/)

#### Pull and run the latest LmRaC image

```         
docker pull dbcraig/lmrac:latest
cd <your-lmrac-root>
docker run -m1024m -it -e OPENAI_API_KEY=${OPENAI_API_KEY} -e PINECONE_API_KEY=${PINECONE_API_KEY} -v $(pwd)/work:/app/user -v /etc/localtime:etc/localtime:ro -p 5000:5000 dbcraig/lmrac
```

Open the [LmRaC Homepage](#LmRaC-Homepage) from <http://localhost:5000>.

### Docker Desktop (Linux / Mac / Windows)

#### Install Docker Desktop

For instructions on how to install Docker Desktop, see:

- [Docker Desktop for Linux](https://docs.docker.com/desktop/install/linux-install/)
- [Docker Desktop for Mac (macOS)](https://docs.docker.com/desktop/install/mac-install/)
- [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/)

#### Pull the latest LmRaC image

From the Docker Desktop search for *dbcraig/lmrac* and then pull the *latest* image. This will copy the latest release of LmRaC to your local machine.

![](img/DockerDesktop_Pull.png)

1. **Search:** Click on the search area to open the Search dialog.
2. **Search dialog:** Search for *dbcraig/lmrac*. Set the Tag dropdown to *latest* (default).
3. **Pull:** Click on the Pull button to download the latest LmRaC image to Docker Desktop.

#### Create a running container from the image

You should now see the dbcraig/lmrac:latest image in the Images view. Highlight this image and click on the Run icon under Actions.

![](img/DockerDesktop_Run.png)

1. **Images view:** Click on Images to see a list of all pulled images.
2. **Run:** Find *dbcraig/lmrac* in the list and click on the run icon (play arrow) to open the run dialog.

#### Container settings

Before running the image set the parameters so that LmRaC has API keys and knows where to find your data.

![](img/DockerDesktop_Settings.png)

A note on terminology: the Docker *image* is a read-only template with all the information needed for creating a running program. An instance of the running program (created from the *image*) is called a *container*. For LmRaC the container is a web server that you can interact with through a browser.

1. **Container name:** (optional) You can give the container (the running program) a name, otherwise Docker Desktop with generate a random name.
2. **Ports:** Enter a "0" for Docker Desktop to generate a random port on which to find the LmRaC application. Though the LmRaC container runs on port 5000, it doesn't know what port the host machine has available. This allows Docker Desktop to assign an available port and map it LmRaC's internal port (this is analogous to how your local directory is mapped to LmRaC's internal /app/user).
3. **Volumes (work directory):** Select the path on your host (the machine running Docker Desktop) that you want to be the user root (*/app/user*) for LmRaC. This allows the container to write files to your host (the machine running Docker Desktop). For security, Docker containers are not allowed to access anything on the host machine *unless* you explicitly map (aka mount) a directory into the container.
4. **Volumes (localtime):** (optional) Time in the container is not necessarily the same as time on the host running Docker Desktop. Mapping the */etc/localtime* insures that the timestamp LmRaC uses to name answers and logs is aligned with the time on your Docker Desktop host.
5. **Environment variables (OpenAI API):** Pass in the literal API key value that LmRaC will use to talk to the OpenAI GPT-4o model.
6. **Environment variables (Pinecone API):** Pass in the literal API key value that LmRaC will use to talk to the Pinecone vector database.
7. **Run:** Press Run to create the running container.

#### Launch the LmRaC application

You should now see the container you just created running in the Containers view.

![](img/DockerDesktop_Launch.png)

1. **Containers view:** Click on Containers to see a list of all containers. This includes running as well as stopped containers. 
2. **Container URL line:** Since LmRaC is a web application and you specified a Port of "0" as part of the [Run configuration](#Container-settings), you will see a hyperlink created by Docker Desktop to launch LmRaC. Click on this to open the browser to see the [LmRaC Homepage](#LmRaC-Homepage).
3. **Stop container:** Once you are done running LmRaC you can clean up be stopping the running container. This frees up CPU and memory on the host.
4. **Delete container:** Stopped containers exist until you delete them since they can be re-started. Note that deleting a container *does not* delete or otherwise affect the image it was created from.

------------------------------------------------------------------------

## LmRaC Homepage

The LmRaC homepage allows the user to interact with LmRaC as well as open sub-windows for experiments, indexes, functions and saved answers.

![](img/LmRaC_main.png)

1.  **LmRaC message area:** Shows all messages from LmRaC as well as user commands and questions.
2.  **User input area:** Where the user types questions and commands for LmRaC.
3.  **Submit:** Button to send the user input to LmRaC.
4.  **Submit on ENTER:** Checkbox that allows the user to send input simply by pressing the Enter key in the user input area (same as clicking on the Submit button). Uncheck this if you want to include linefeeds in your input.
5.  **Help:** Button to prompt the user to type "help" in the user input area.
6.  **Erase:** Button to clear the LmRaC message area.
7.  **Download:** Button to allow the user to download the entire contents of the LmRaC message area to a file.
8.  **Answers:** Button to open the Answers window from which all saved answers can be viewed.
9.  **Experiments:** Button to open the Experiments window which shows all available experiments.
10. **Indexes:** Button to open the Indexes window which shows all available indexes.
11. **Functions** Button to open the Functions window which shows all available function libraries.

### Commands
Although the user input area is typically used to ask questions, it can also be used to enter commands. LmRac understands the following commands:

#### Help Commands
- **Help**  A summary of available help.
- **Help indexes**  General information about indexes.
- **Help experiments**  General information about experiments. 
- **Help functions**  General information about functions.
- **Help questions**  General information about asking questions.
- **Help examples**  Some sample questions you can ask.
  
#### Index Commands
- **Set current index to** *\<index-name\>*  Set/create the index for answering questions.
- **Show current index**  Show the name of the current index.
- **List indexes**  List the available indexes.
  
#### Experiment Commands
- **Set current experiment to** *\<experiment-name\>*  Set/create an experiment folder.
- **Show current experiment**  Show the name of the current experiment.
- **List experiments**  List the available experiments.
  
#### Function Commands
- **Load function** *\<function-name\>*  Make a function library unavailable for question answering.
- **Unload function** *\<function-name\>*  Make a function library available for question answering.
- **List available functions**  List function libraries that have been successfully compiled and are available to be loaded.
- **List loaded functions**  List function libraries that will be used when answering questions.
- **Set REST API IP**  Set the IP and port on which LmRaC will make function requests to the user-defined REST API server.
  
#### Other Commands
- **Show configuration**  Show the current configuration and settings.
- **Load experiment documents to** *\<experiment-name\>*  Manually load and compute embeddings for a document then save it to an experiment. User will be prompted for the file name.
- **Enable/Disable debug messages**  Show verbose function calls and intermediate results. Can be useful for rephrasing more complex questions.
- **Quit**  Save the current configuration and shutdown the homepage and server.

Note that commands should be asked one at a time. Also, LmRaC currently does not remember previous commands or questions.

------------------------------------------------------------------------

## Indexes Window

The Indexes window can be opened by clicking on the Indexes button on the [LmRaC Homepage](#LmRaC-Homepage).

![](img/LmRaC_Indexes.png)

Available indexes are listed with the current index, if any, selected. Select an index by clicking on its radio button. This is equivalent to asking LmRaC on the [LmRaC Homepage](#LmRaC-Homepage) to set the index.

Hovering over the information icon displays the index description, if any, from when the index was created.

Only one index may be selected at a time.

------------------------------------------------------------------------

## Experiments Window

The Experiments window can be opened by clicking on the Experiments button on the [LmRaC Homepage](#LmRaC-Homepage).

![](img/LmRaC_Experiments.png)

Available experiments are listed with the current experiment, if any, selected. Select an experiment by clicking on its radio button. This is equivalent to asking LmRaC on the [LmRaC Homepage](#LmRaC-Homepage) to set the experiment.

Hovering over the information icon displays the experiment description, if any, from when the experiment was created.

Clicking on the folder icon shows the contents of the experiment folder: files in the experiment root, and the *docs/* folder, if any. The *docs/* folder is where [saved answers](#Saving-Answers-to-Experiments) and [uploaded experiment documents](#Manual-document-upload) are saved.

Only one experiment may be selected at a time.

------------------------------------------------------------------------

## Functions Window

The Functions window can be opened by clicking on the Functions button on the [LmRaC Homepage](#LmRaC-Homepage).

![](img/LmRaC_Functions.png)

Available functions are listed with all loaded functions, if any, checked. Load a function by clicking on its checkbox. This is equivalent to asking LmRaC on the [LmRaC Homepage](#LmRaC-Homepage) to load the function. Unload the function by unchecking.

Hovering over the information icon displays the function DESCRIPTION, if any, from the function definition file (*.fn*).

Any number of functions may be loaded. However, keep in mind that all loaded functions are passed to GPT4 when asking *any* question. This allows GPT4 to make use of any loaded function when answering a question, but increases the number of input tokens. So, if a function is not needed, do not load it. This improves the accuracy of the answer and reduces cost.

------------------------------------------------------------------------

## Answers Window

The Answers window can be opened by clicking on the Answers icon on the [LmRaC Homepage](#LmRaC-Homepage).

![](img/LmRaC_Answers.png)

1. **Search** can be used to select only answers with the specified text in either the question or the answer (search is case insensitive).
2. **Timestamp** shows the date and time of the session an answer was created along with a sequence number for the anwer within that session.
3. **Question** text shows the original question.
4. **Answer Summary** can be shown by hovering over the info icon.
5. **Assessment** of the qualify of a general question (not experiment questions) can be shown by hovering over the ribbon icon.
6. **MD** button opens the full text of the answer as a markdown document. See [Markdown Viewing](#Markdown-Viewing) for how to setup your browser to automatically display markdown.
7. **HTML** button opens the full text of the answer as an HTML document.
8. **Test Tube** icon is used to select answers for saving to experiments.
9. **Download** icon is used to download the full text of the answer as a markdown document.

Once you select one or more answers (by clicking on the test tube), the answers save dialog opens in the Answers window.

![](img/LmRaC_Answers_save.png)

### Saving Answers to Experiments
Click on the test tube next to the answer you want to add. The test tube will be highlighted with a check mark. You may select as many answers as you wish (see Red outline).

1. Select the destination Experiment name (the current experiment, if any, will have an '*' next to its name).
2. Select the Index for the document embeddings. Remember that these documents will only be searchable when this index set as current.
3. Once both the Experiment and Index have been selected, click on the copy documents icon.

Answers are copied to the experiment *docs/* folder and added to the index (i.e., embeddings computed) in the background. This typically takes less than a minute to complete.

------------------------------------------------------------------------

## Configuration

If no user configuration is supplied, LmRaC will use the following defaults. Note that the root /app/user/ is how the container sees your mounted volume. So, if ~/my-directory/lmrac-work/ is mounted when starting Docker, this will be /app/user/

```         
Session Logs Directory  : /app/user/sessions/
Final Answers Directory : /app/user/sessions/finalAnswers/
Experiments Directory   : /app/user/experiments/
Vocabularies Directory  : /app/user/vocab/
Functions Directory     : /app/user/
Indexes Directory       : /app/user/
Vocab Directory         : /app/user/
  Vocab Genes           : hgnc_complete_set.symbol.name.entrez.ensembl.uniprot.tsv
  Vocab Pathways        : KEGG.pathways.refs.csv
  Vocab Diseases        : MESH.diseases.csv

Functions REST API IP   : 172.17.0.2:5001
```

In addition, default vocabulary files for genes, diseases and pathways will be copied into the vocab/ folder.

When quitting LmRaC the configuration is saved to *config/LmRaC.config*

### Markdown Viewing

LmRaC answers use [standard Markdown](https://www.markdownguide.org/getting-started/) to improve readability and add hyperlinks (e.g., to citations). Although you can use a dedicated Markdown editor or note-taking application to view LmRaC answers, you can also use a browser extension/add-on to automatically render Markdown in your favorite browswer.

[Markdown Viewer](https://github.com/simov/markdown-viewer) is a browser extension compatible with all major browsers. Follow the simple install instructions for your browser then from ADVANCED OPTIONS for the extension [enable Site Access](https://github.com/simov/markdown-viewer?tab=readme-ov-file#enable-site-access) for the LmRaC URL:

![](img/MarkdownViewer.png)

------------------------------------------------------------------------

## Usage - Q and A

LmRaC is specifically designed to answer questions regarding genes, disease and biological pathways. It does this by searching [NIH PubMed](https://pubmed.ncbi.nlm.nih.gov/) for related journal articles. Articles are indexed using text embeddings and tagged with metadata corresponding to their search (e.g., KEGG, MeSH or gene identifiers). 

### Setting an Index

The **index** is the vector database used to search for related information. LmRaC does not answer questions using GPT4's knowledge, instead it searches PubMed for related publications and then assembles this information into an answer. This virtually eliminates any chance of hallucinations. Initially, an index is empty. It is then populated as questions are asked about particular genes, diseases and/or pathways.

### Asking a Question

Questions are evaluated to determine what, if any, genes, diseases and/or pathways are explicitly -- or, in some cases, implicitly -- mentioned. Identified terms are then matched against vocabulary lists for each type to associate terms with unique identifiers which can then be used as metadata for subsequent searches.

The detail of an answer is determined by a number between 1 and 7 with 1 answering the question only. Detail of 2-7 generated sub-questions related (in the opinion of GPT4) to the original question. Once the original question and all sub-questions have been answered, they are edited into a single final answer along with paragraph level citations to all sources used in answering the question.

Feedback is also provided by GPT4 on the accuracy and completeness of the answer.

### Providing PubMed Sources

When a term is not recognized (i.e., no embedding has the identifier as metadata), the user is given the option to search PubMed for associated journal articles. These are then analyzed and embeddings stored in Pinecone for subsequent searches. While pathways and diseases initiate a single search, pathways are searched in two stages. In the first stage publications used in the curation of the pathway (these references are part of KEGG) are used as "primary" sources. Citations to each of these primary sources are then collected from PubMed as "secondary" sources. Secondary sources represent the results of more recent research.

### Tips

> **What's Enough?** Do not feel you must populate an index with hundreds of articles. Often, answers require only a few articles. Since searches return results sorted by relevance, it is often sufficient to only download 10 of the best citations to answer most common questions.

> **Pathway References:** When asking a question about pathways in particular, explicitly mention the pathway. For example, "How is smoking related to the NSCLC pathway?" is more likely to reference both the pathway for NSCLC (KEGG [hsa0522](https://www.genome.jp/pathway/hsa05223)) and the disease (MeSH [D002289](https://meshb.nlm.nih.gov/record/ui?ui=D002289)).

> **How Detailed?** More detailed answers aren't always better. Since the requested complexity (i.e., detail) determines the number of sub-questions generated, detail should be correlated with the complexity of the question, otherwise LmRaC will likely generate significantly redundant answers. Ask for more detail when there are expected implicit questions in the original question.

------------------------------------------------------------------------

## Usage - Experiments

A key feature of LmRaC is its ability to answer questions about a user's own experiments and data. Two components make this possible:

- a user-defined experimental context of documents and data
- user-defined functions that answer questions about that data

The context is simply an index, like those created for general questions, that focuses on information about the experiment. Function are user provided code that retrieves or otherwise manipulates data so that it is available to answer a question. A user needed "call" the function explicitly, he or she need only describe it and then leave it to LmRaC to use the function if it will aid in answering a question.

### Experimental Results

For example, assume you have an experiment where you have measured differentially expressed genes (DEG) between affected subjects and unaffected subjects. Typically, this type of experiment results in a file that contains all measured genes, how much they changed between experimental conditions, and if this change was statistically significant. You could ask:

```
[user]  What is the expression of BRCA1 in my experiment?
[LmRaC] The expression of the gene **BRCA1** in your experiment "greatStuff" is as follows:
- **Log Fold Change (logFC):** 1.488
- **Adjusted p-value (adjP):** 0.000001
```



### Creating an experimental context

When asking questions about experiments LmRaC will first search for documents indexed for the experiment. This means documents in the experiment's *docs/* folder. These are either saved answers or uploaded documents (see below). In either case these documents have been copied to the *docs/* folder and, most importantly, had their embeddings computed so that they are available for search.

Creating a context, therefore, means creating a group of documents that provide a focused knowledge base relative to the experiment. This can be background documents on genes, pathways and diseases generated from general questions. It can also include relevant protocol or other background documents that provide details relevant to interpreting your experimental results.

Importantly, one of the strengths of LmRaC is that though it will use this experimental context, it can also search the general literature. Keep this in mind when formulating your questions.

**IMPORTANT** Experiment documents are "authoritative" when asking experimental questions. LmRaC does not implicitly use GPT4 to validate or otherwise confirm the veracity of any document that is uploaded. Therefore, for example, if you upload experiment documents that provide evidence that the world is flat, expect answers to use this "fact." You are the author of your experimental findings!

#### Saving Answers to Experiments

From the [Answers Window](#Answers-Window) select any answers you want saved to a specific experiment. Select an index. Click on the copy documents icon. Keep in mind that when an answer is saved to an experiment, the text of the answer is saved in the experiment directory, but the embeddings (i.e., searchable meaning) are saved in an index along with metadata that links it to the experiment. When asking questions about the experiment, you must use this index.

#### Manual document upload

Documents can also be uploaded to experiments manually. Simply ask LmRaC to "load experiment document to *< experiment >*". You will be prompted for the document name. Once copied to the experiment's *docs/* folder, embeddings will be computed and added to the current index. This makes the document available for questions. 

Although it is possible to simply copy documents into the experiment's *docs/* folder, embeddings will not be computed, therefore, the documents are not searchable when asking questions about the experiment. Use the "load experiment documents" command to make the document available for search.

**IMPORTANT** Docker containers can only see directories that have been mounted using the **-v** command. This means the path to upload documents is relative to the container's mount point. For example, if you run the LmRaC container with **-v $(pwd)/work:/app/user**, LmRaC can only see folders in the work/ directory tree. These are referenced in the container as */app/user*. So, if you want to load a document from *work/my-docs/experimentInfo.txt*, the full path when using the LmRaC load command would be */app/user/my-docs/experimentInfo.txt*.

------------------------------------------------------------------------

## Usage - User-Defined Functions

xxx
Key to LmRaC is its easy extensibility, that is, the user's ability to add functionality ...
... not only data manipulation, but also API interface to other resources
making this information immediately available for answering questions

A complete functional API is provided in this GitHub repository...

### Setting up the REST API Server

Clone the base REST API server from this GitHub repository, then build the Docker image for the functions server.

```         
git clone https://github.com/dbcraig/LmRaC.git
docker build -t lmracrest:latest .
```

Run the functions REST API server:

```         
cd <your-lmrac-root>
docker run -it -v $(pwd)/work:/app/user -p 5001:5001 lmracrest
```

When the server starts up it will show the IP:port on which it is running.

LmRaC must know this IP:port in order to make function requests. You can edit the LmRaC.config file (see [Configuration](#configuration)) so that the *functionsREST* key value is set to IP:port (e.g., "172.17.0.2:5001") or you can set the IP:port dynamically be asking LmRaC to set the value (e.g., "Please set the functions REST API IP and port to 172.17.0.2:5001")

#### REST API Server Docker image

xxx
If you want to try the server without building it...
this is a built version of what is in the source repository, so only has basic functionality

### Adding Functions (Server - REST Server)

xxx
See DEGbasic.py

Required parts:

- xx
- xx

### Using Functions (Client - LmRaC)

xxx

#### Function prototypes (interface definition)

xxx
Since LmRaC is a language model, it relies on descriptions of functions and parameters ...

```
#
#	Line comments begin with a '#' mark
#
DESCRIPTION	"This describes the entire group of functions and is used to create a README file"

FUNCTION initializeMyFunctions      "Functions dont have to have any parameters"

# indentation is not necessary and is only used for readability; extra tabs and spaces are ignored
# all lines must have a "comment" value since these are used by LmRaC to interpret and assign values

FUNCTION getTopExpressionResults    "This text describes the what the function does and is how LmRaC decides to use it"
    PARAMETER topK:NUMBER           "The NUMBER type may be integer or float depending on the function implementation"
    PARAMETER byFoldChange:BOOLEAN  "The BOOLEAN type is true or false"
    PARAMETER experiment:STRING     "STRING type are for characters"
    PARAMETER filename:STRING*      "Adding a '*' makes the parameter optional"
    PARAMETER geneArray:ARRAY       "ARRAY types can contain any type item except another array"
        ITEM gene:STRING            "array items begin with the ITEM keyword"
```

#### Function compilation

xxx

#### Function loading

xxx Load the function ... it will be used based on the description

xxx Errors when loading... LmRaC tests that the JSON is well formed
... show (!) message ?

Why unload a function

### General Functions

xxx
Can they be used to extend the functionality of LmRaC ??

------------------------------------------------------------------------

## Indexes and Experiments and Functions

Indexes are purposely independent of Experiments.

Functions are purposely independent of Experiments.

With flexibility comes responsibility. Maybe the most confusing part of LmRaC is remembering that indexes and experiments independent. Think of indexes as a collection of information about a domain of knowledge *that you define.* Within that collection is additional information about particular experiments (e.g., answers you've saved, documents you've uploaded, interpretations of results). So, if you want to ask questions (i.e., search) about these experiments, you need to use this index.

However, information about an experiment can be saved to *more than one index*! You may have an index created specifically for one disease (e.g., breast cancer). You may have another index created for a particular experimental protocol (e.g., differential gene expression). Information about your experiment investigating gene expression in breast cancer can be saved to both indexes! *Or*, you could just create one large index for both breast cancer and differential gene expression. You have the flexibility to design the knowledge base best suited for the questions you ask.

Likewise, functions are designed to manipulate your data (e.g., read, search, compute). You can group them any way you like and use them in any combination. They are not part of an experiment. They are only there to aid in answering questions about the experiment.

------------------------------------------------------------------------

## Troubleshooting

> **LmRaC isn't calling my function:** The most common cause for this is that the function has not been loaded. Although function files are read and compiled at initialization, they must also be *loaded* in order to be available for questions. This allows LmRaC to focus only on functions relevant to the task at hand. Note that what functions are loaded is saved to the configuration file, so after restarting LmRaC your functions are automatically re-loaded.

> **Memory:** Because LmRaC uses multiprocessing extensively, complex questions can require significant memory resources while documents are being processed. We recommend a minimum of 1GB for the Docker container, though 2GB may be necessary for large multi-part questions. The error **A process in the process pool was terminated abruptly while the future was running or pending** is usually an indication that LmRaC ran out of memory.

> **Rate Limits:** All servers have rate limits (i.e., maximum number of requests per second). In the case of PubMed this is fix. For OpenAI this increases over time for users. In all cases LmRaC will retry a request in the event of a rate limit error. Retries employ an exponential backoff strategy that, in most cases, is sufficient for the request to ultimately succeed. As a consequence, users may see slower response times when using LmRaC with a new OpenAI account.

> **Low Assessment Scores:** Note that it is not unusual for GPT4 to assess final answers as poor. Most often this is due to two factors: (1) GPT4 flags citations as "fake" because they occur after the training cutoff date of GPT4; or, (2) GPT4 objects to the complexity of the answer as exceeding the scope of the original question, or inappropriate for a lay audience. On the other hand, these assessment often offer insightful critiques that may prompt further questions.

------------------------------------------------------------------------

## How To Cite

*Coming Soon!* Currently under review.

## Contact

Douglas Craig : <craigdou@med.umich.edu>
