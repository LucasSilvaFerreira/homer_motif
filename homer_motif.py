
def install_homer_colab_hg19():
  !wget http://homer.ucsd.edu/homer/configureHomer.pl
  !perl configureHomer.pl -install hg19
  x_p = !echo $PATH
  final_p  = x_p[0] + ':/content/.//bin/' 
  %env PATH= $final_p
  


def create_one_by_one_motif(bed_file, out_name ):
  df_process_one = pd.read_csv(bed_file, sep='\t')
  
  df_process_one['3'] = df_process_one[['0','1','2']].apply(lambda x : '_'.join(map(str,x)) ,axis=1)
  bed_file_use = 'tag_added_' + bed_file
  df_process_one.to_csv(bed_file_use,
                         index=None,
                         header=None, sep='\t')
  set_cell = dict(zip(df_process_one['3'].values, df_process_one['4'].values))
  # print (df_process_one)
  # print (out_name)
  cmd = f'perl bin/findMotifsGenome.pl   {bed_file_use}  data/genomes/hg19    "{out_name}"   -find  data/knownTFs/vertebrates/known.motifs  -p 4 -nomotif -size 1000 >teste.txt'
  !$cmd
  df_vertebrates_motif = pd.read_csv('teste.txt', sep='\t')
  # df_vertebrates_motif['sig'] = df_vertebrates_motif['PositionID'].apply(lambda x :  'non_sig' if "non" in x  else 'sig' )
  # df_vertebrates_motif['abs_offset'] = np.abs(df_vertebrates_motif['Offset'])
  # df_vertebrates_motif = df_vertebrates_motif.sort_values(['sig', 'abs_offset'])
  # df_vertebrates_motif['color'] = df_vertebrates_motif['sig'].apply(lambda x : 'red' if x == 'sig' else 'gray')
  df_vertebrates_motif.drop_duplicates(['PositionID', 'Motif Name']).groupby('PositionID')
  df_vertebrates_motif['cell_tag'] = df_vertebrates_motif['PositionID'].apply(lambda x : set_cell[x])
  df_vertebrates_motif['bed_tag'] = out_name
  return df_vertebrates_motif