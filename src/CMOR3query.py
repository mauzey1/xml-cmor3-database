#!/bin/env python
from __future__ import print_function

import sqlite3
import json
conn = sqlite3.connect('./CMIP6.sql3')
c = conn.cursor()

# =======================================================================
#                               getMIPs()                             
# =======================================================================
def getMIPs():
    '''
    Extract all MIPs
    '''
    cmd= """select DISTINCT m.label from MIP m;"""
    c.execute(cmd)
    MIPS=c.fetchall()
    return MIPS

# =======================================================================
#                        getExperimetnGroups()
# =======================================================================
def getExperimentGroups(MIP):
    '''
    Retrieve Experiment Groups and Experiments requested by a MIP
    '''
# sqlite> select DISTINCT eg.label, eg.uid from exptGroup eg, requestItem ri where ri.mip='CFMIP' and ri.esid = eg.uid order by eg.label;

    cmd="""select DISTINCT eg.uid 
           from exptGroup eg, 
                requestItem ri 
           where  ri.mip='""" + MIP + """' and 
                  eg.uid=ri.esid 
           order by eg.label;"""
    c.execute(cmd)
    ExptGroups = c.fetchall()
    return ExptGroups
# =======================================================================
#                    getExperimentGroupUID()
# =======================================================================
def getExperimentGroupUID(Label):
    '''
    Retrive Experiment Group UID from Label
    '''
    cmd="""select DISTINCT eg.uid
            from exptGroup eg
	    where  eg.label='"""+Label+"""';"""

    c.execute(cmd)
    ExptGroupUID = c.fetchall()
    return ExptGroupUID[0][0]

# =======================================================================
#                    getExperimentGroupLabel()
# =======================================================================
def getExperimentGroupLabel(exptGroupUID):
    '''
    Retrieve Experiment Groups Label
    '''
    cmd="""select DISTINCT eg.label
            from exptGroup eg
	    where  eg.uid='"""+exptGroupUID+"""';"""

    c.execute(cmd)
    ExptGroupLabel = c.fetchall()
    return ExptGroupLabel[0][0]

# =======================================================================
#                        getExperimentLabel()
# =======================================================================
def getExperimentLabel(experimentUID):
    '''
    Retrieve Experiment Label
    '''
    cmd="""select DISTINCT ex.label
            from experiment ex
	    where  ex.uid='"""+experimentUID+"""';"""

    c.execute(cmd)
    ExptGroupLabel = c.fetchall()
    return ExptGroupLabel[0][0]

# =======================================================================
#                           getExperimentUID()
# =======================================================================
def getExperimentUID(experimentLabel):
    '''
    Retrieve Experiment Identifier
    '''
    cmd="""select DISTINCT ex.uid
            from experiment ex
	    where  ex.label='"""+experimentLabel+"""';"""

    c.execute(cmd)
    ExptGroupUID = c.fetchall()
    return ExptGroupUID[0][0]


# =======================================================================
#                getExperimentsbyExptGroupID()
# =======================================================================
def getExperimentsbyExptGroupID(exptGroupUID,MIP):
    '''
    Retrieve experiments from an experiment group ID.
    '''
#sqlite> select DISTINCT ex.label from requestItem ri, experiment ex, exptGroup eg where ex.mip='CFMIP' and eg.uid=ex.egid and eg.uid=ri.esid and eg.label='Cfmip4' order by eg.label;

    exptGroupLabel = getExperimentGroupLabel(exptGroupUID)
    cmd="""select DISTINCT ex.uid
            from exptGroup eg,
                 experiment ex,
                 requestItem ri
	    where ex.mip='"""+MIP+"""' and
                  eg.uid = ex.egid and
                  eg.uid = ri.esid and
                  eg.label = '""" + exptGroupLabel + """'
            order by eg.label"""
    c.execute(cmd)
    Experiments= c.fetchall()
    return Experiments

# =======================================================================
#               getExperimentsbyExptGroupLabel()
# =======================================================================
def getExperimentsbyExptGroupLabel(exptGrpLabel,MIP):
    '''
    Retrieve experiments from an experiment group Label.
    '''
#sqlite> select DISTINCT ex.label from requestItem ri, experiment ex, exptGroup eg where ex.mip='CFMIP' and eg.uid=ex.egid and eg.uid=ri.esid and eg.label='Cfmip4' order by eg.label;

    exptGroupUID = getExperimentGroupUID(Label)
    cmd="""select DISTINCT ex.label
            from exptGroup eg,
                 experiment ex,
                 requestItem ri
	    where ex.mip='"""+MIP+"""' and
                  eg.uid = """+exptGroupUID+""" and
                  eg.uid = ri.esid and
                  eg.label = '""" + exptGrpLabel + """'
            order by eg.label"""
    c.execute(cmd)
    Experiments= c.fetchall()
    return Experiments

# =======================================================================
#                                getGrid()
# =======================================================================
def getGrid(structureID):
    '''
    Retrieve structure grid from stid
    '''
    cmd="select s.spid,s.tmid,s.cell_measures, s.cell_methods from structure s where s.uid == '" + structureID +"';"
    c.execute(cmd)
    data=c.fetchone()
    return data        

# =======================================================================
#                              getSpatialShape()
# =======================================================================
def getSpatialShape(spatialID):
    '''
    Retrieve XYZ grid from spatialShape table

    Return dimensions, levelFlag and levels
    '''
    # ----------------------
    # Extract Spatial dimension
    # ----------------------
    cmd="select ss.dimensions, ss.levelFlag, ss.levels from spatialShape ss where ss.uid == '" + spatialID +"';"
    c.execute(cmd)
    spatial=c.fetchone()
    return spatial

# =======================================================================
#                              getTemporalShape()
# =======================================================================
def getTemporalShape(spatialID):
    '''
    Retrieve time dimension from temporalShape table

    return dimension and label
    '''
    # ----------------------
    # Extract Time dimension
    # ----------------------
    cmd="select ts.dimensions, ts.label from temporalShape ts where ts.uid == '" + spatialID +"';"
    c.execute(cmd)
    temporal=c.fetchone()
    return temporal

# =======================================================================
#                             getVariables()
# =======================================================================
def getVariables(MIP,exptGroupLabel,experimentLabel):
    '''
    Get all variables requested by an experiment group

    return GridUID, label, frequency, mipTable, modeling_real, ok_max_mean_abs, ok_min_mean_abs, positive, valid_max, valid_min, group_label, experiment_label.
    '''
    exptGroupUID = getExperimentGroupUID(exptGroupLabel)
    exptUID      = getExperimentUID(experimentLabel)
    cmd="""select DISTINCT v.stid, 
			   v.label,
			   v.frequency, 
			   v.mipTable, 
			   v.modeling_realm, 
			   v.ok_max_mean_abs, 
			   v.ok_min_mean_abs, 
			   v.positive, 
			   v.valid_max, 
			   v.valid_min,
                           eg.label,
                           ex.label
	    from experiment ex, 
                 exptGroup eg, 
                 requestVar rv, 
                 requestVarGroup rvg, 
                 requestItem ri, 
                 requestlink rl, 
                 CMORvar v 
	    where  ri.mip='"""+MIP+"""'  and 
                   eg.uid='"""+exptGroupUID+"""' and 
                   ex.uid='"""+exptUID+"""' and 
                   eg.uid=ri.esid and
		   ri.rlid=rl.uid   and 
		   rl.refid=rvg.uid and 
		   rvg.uid=rv.vgid  and 
		   v.uid=rv.vid
            order by eg.label,ex.label;"""
    c.execute(cmd)
    variables = c.fetchall()
    return variables

# =======================================================================
#                   convertVarStructureToDictionary()
# =======================================================================
def convertVarStructureToDictionary(variable):
    '''
       Take a variable query result and convert it to a dictionary
    '''
    varDict = {'gridID':            variable[0],
	       'label':             variable[1],
               'frequency':         variable[2],
               'mipTable':          variable[3],
               'modeling_realm':    variable[4],
	       'ok_max_mean_abs':   variable[5],
	       'ok_min_mean_abs':   variable[6],
	       'positive':          variable[7],
	       'valid_max':         variable[8],
	       'valid_min':         variable[9],
               'exptGroupLabel':    variable[10],
               'experimentLabel':   variable[11]
             }
    return varDict

# =======================================================================
#                               QueryAmon()
# =======================================================================
def QueryAmon(MIP):
    '''
    '''
    pass 

# =======================================================================
#                                QueryAll()
# =======================================================================
def QueryAll():
    '''
       Query all MIPS ExperimentGroups experiments and variables
    '''
    MIPs = getMIPs();
    cmor3Table={}
    cmor3Table['MIPs'] = {}
    for MIP in MIPs:
        cmor3Table['MIPs'][MIP[0]] = {}
        cmor3Table['MIPs'][MIP[0]]['experimentGroups'] = {}
        exptGroups = getExperimentGroups(MIP[0])
        for exptGroup in exptGroups:
            exptGroupLabel =  getExperimentGroupLabel(exptGroup[0])
            cmor3Table['MIPs'][MIP[0]]['experimentGroups'][exptGroupLabel] = {}
            cmor3Table['MIPs'][MIP[0]]['experimentGroups'][exptGroupLabel]['experiments'] = {}
            experimentsDict = cmor3Table['MIPs'][MIP[0]]['experimentGroups'][exptGroupLabel]['experiments'] 
            experiments =  getExperimentsbyExptGroupID(exptGroup[0],MIP[0])
            for experiment in experiments:
                experimentLabel =  getExperimentLabel(experiment[0])
                experimentsDict[experimentLabel]= {}
                experimentsDict[experimentLabel]['variables'] = {}
                variablesDict=experimentsDict[experimentLabel]['variables'] 
                variables=getVariables(MIP[0],exptGroupLabel,experimentLabel)
            for variable in variables:
                    grid = getGrid(variable[0])
                    spatialShape = getSpatialShape(grid[0])
                    temporalShape = getTemporalShape(grid[1])
                    varDict = convertVarStructureToDictionary(variable)
            # Print Report
            # ----------------------
                    variablesDict[varDict['label']] = {}
                    currentVarDict=variablesDict[varDict['label']]
                    currentVarDict['frequency']         = varDict['frequency']
                    currentVarDict['mipTable']          = varDict['mipTable']
                    currentVarDict['modeling_realm']    = varDict['modeling_realm']
                    currentVarDict['ok_max_mean_abs']   = varDict['ok_max_mean_abs']
                    currentVarDict['ok_min_mean_abs']   = varDict['ok_min_mean_abs']
                    currentVarDict['positive']          = varDict['positive']
                    currentVarDict['valid_max']         = varDict['valid_max']
                    currentVarDict['valid_min']         = varDict['valid_min']
                    currentVarDict['cell_measures']     = grid[2]
                    currentVarDict['cell_methods']      = grid[3]
                    currentVarDict['dimensions']        = spatialShape[0]
                    currentVarDict['levelFlag']         = spatialShape[1]
                    currentVarDict['levels']            = spatialShape[2]
                    currentVarDict['timeDimension']     = temporalShape[0]
                    currentVarDict['timeLabel']         = temporalShape[1]
    c.close()
    print(json.dumps(cmor3Table, indent=4))

        # ----------------------
        # Extract all variables
        # ----------------------
    #select DISTINCT eg.label,ex.label from requestItem ri, experiment ex, exptGroup eg where ex.mip='CFMIP' and eg.uid=ex.egid and eg.uid=ri.esid order by eg.label;^C

