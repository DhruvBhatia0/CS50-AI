import os
import random
import re
import sys
import math

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    temp_total = 0
    for page in ranks.keys():
        temp_total += ranks[page]
    print(temp_total)
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    temp_total = 0
    for page in ranks.keys():
        temp_total += ranks[page]
    print(temp_total)


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    '''
    prob for a page linked to from current page:
    damping_factor*(1/number of pages linked) + 1-damping_factor/total number of pages
    prob for other pages:
    1-damping_factor/total number of pages
    '''
    corpus = dict(corpus)
    #check if the page links to anyone
    if corpus[page] == set():
        temp = dict()
        for i in corpus.keys():
            temp[i] = 1/len(corpus.keys())
        return temp
    distribution = dict()
    for i in corpus[page]:
        distribution[i] = damping_factor*(1/len(corpus[page])) + (1-damping_factor)/len(corpus.keys())
    for i in corpus.keys():
        if i not in corpus[page]:
            distribution[i] = (1-damping_factor)/len(corpus.keys())
    return distribution



def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    '''
    have a dictionary to store the number of times the user vists a page
    have a system that visits a random page based on the distribution given by transition_model()
    '''
    corpus = dict(corpus)
    counter = dict()
    for page in corpus.keys():
        counter[page] = 0
    #every page has been visted 0 times
    pages = list(corpus.keys())
    a = random.randint(0,len(pages)-1)
    current_page = pages[a]
    for _ in range(n):
        counter[current_page] += 1
        a = random.randint(1,1000)/1000
        temp = 0
        distribution = transition_model(corpus, current_page, damping_factor)
        for page in distribution.keys():
            temp += distribution[page]
            if temp >= a:
                current_page = page
                break
    
    for page in counter.keys():
        counter[page] = counter[page]/n
    return counter

    


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    '''
    make a dictionary with every page and a rank
    give every page a rank of 1/len(dict.keys())
    iterate through every page and use the formula once
    repeat the above step 100 times
    for some insight, print the values every 10 loops
    '''
    corpus = dict(corpus)
    page_rank = dict()
    for page in corpus.keys():
        page_rank[page] = 1/len(corpus)
    for i in range(100):
        for page in page_rank.keys():
            probability = 0
            for connected in corpus[page]:
                temp = len(corpus[connected])
                if temp == 0:
                    temp = 1
                probability += page_rank[connected]/temp
            page_rank[page] = (1-damping_factor)/len(corpus.keys()) + damping_factor*probability
    return page_rank
    

if __name__ == "__main__":
    main()
