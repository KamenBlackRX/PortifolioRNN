class Word2Vec:
  '''
  vocab, embeddings
  '''
  def vocab_size(self):
    return len(self.vocab)
  
  def embed_dim(self):
    return len(self.embeddings[0])
  
  def __init__(self, filename):
    import gzip, StringIO
    self.vocab = [PADWORD]
    self.embeddings = [0]
    with file_io.FileIO(filename, mode='rb') as f:
      compressedFile = StringIO.StringIO(f.read())
      decompressedFile = gzip.GzipFile(fileobj=compressedFile)
      for line in decompressedFile:
        pieces = line.split()
        self.vocab.append(pieces[0])
        self.embeddings.append(np.asarray(pieces[1:], dtype='float32'))
    self.embeddings[0] = np.zeros_like(self.embeddings[1])
    
    self.vocab.append('') # for out-of-value words
    self.embeddings.append(np.ones_like(self.embeddings[1]))
    self.embeddings = np.array(self.embeddings)
    print('Loaded {}D vectors for {} words from {}'.format(self.embed_dim(), self.vocab_size(), filename))