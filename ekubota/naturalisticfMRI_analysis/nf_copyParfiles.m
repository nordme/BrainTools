function nf_copyParfiles

subList = {'PREK_1112','PREK_1676','PREK_1691','PREK_1715','PREK_1762',...
    'PREK_1901','PREK_1916','PREK_1951','PREK_1964'};
visitDates = {'20190525','20190525','20190525','20190525','20190525',...
    '20190524','20190524','20190525','20190525'};

parDir = '/home/ekubota/git/BrainTools/ekubota/naturalisticfMRI_analysis';
for ii = 1:length(subList)
    dataDir = strcat('/mnt/scratch/PREK_Analysis/',subList{ii},'/',visitDates{ii},...
        '/fmri/Stimuli/parfiles');
    copyfile(fullfile(parDir,'run3.par'),dataDir)
    cd(dataDir)
    movefile('run3.par','run1.par');
    copyfile(fullfile(parDir,'run3.par'),dataDir)
    movefile('run3.par','run2.par');

end     
