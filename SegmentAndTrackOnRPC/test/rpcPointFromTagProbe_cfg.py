import FWCore.ParameterSet.Config as cms

process = cms.Process("RPCAnalysis")

process.load('Configuration/StandardSequences/Services_cff')
process.load('FWCore/MessageService/MessageLogger_cfi')
process.load("Configuration.StandardSequences.GeometryDB_cff")
#process.load("Configuration.Geometry.GeometryIdeal2015Reco_cff")
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
from Configuration.AlCa.autoCond_condDBv2 import autoCond
#process.GlobalTag.globaltag = autoCond['run2_mc']
process.GlobalTag.globaltag = autoCond['run2_data']

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True),
    allowUnscheduled = cms.untracked.bool(True),
)
process.MessageLogger.cerr.FwkReport.reportEvery = 50000
process.source = cms.Source("PoolSource", fileNames = cms.untracked.vstring())

process.source.fileNames = [
    '/store/data/Run2016B/SingleMuon/RECO/PromptReco-v2/000/273/450/00000/FE30AAEE-381C-E611-A67D-02163E01421E.root',
]

process.goodVertices = cms.EDFilter("VertexSelector",
    src = cms.InputTag("offlinePrimaryVertices"),
    cut = cms.string("!isFake && ndof > 4 && abs(z) <= 24 && position.rho < 2"),
    filter = cms.bool(True),
)

process.load("RPCDPGAnalysis.SegmentAndTrackOnRPC.rpcPointFromTagProbeProducer_cff")
process.rpcPointFromTagProbe.vertex = "goodVertices"

process.load("RecoLocalMuon.RPCRecHit.rpcPointProducer_cff")
process.rpcPointProducer.dt4DSegments = "dt4DSegments"
process.rpcPointProducer.cscSegments = "cscSegments"

process.rpcPoint = cms.EDAnalyzer("RPCPointNtupleMaker",
    doTree = cms.untracked.bool(False),
    doHist = cms.untracked.bool(True),
    vertex = cms.InputTag("goodVertices"),
    rpcRecHits = cms.InputTag("rpcRecHits"),
    refPoints = cms.VInputTag(
        cms.InputTag("rpcPointProducer:RPCDTExtrapolatedPoints"),
        cms.InputTag("rpcPointProducer:RPCCSCExtrapolatedPoints"),
    ),
)

process.tpPoint = process.rpcPoint.clone(
    refPoints = cms.VInputTag(
        cms.InputTag("rpcPointFromTagProbe"),
    ),
)

process.TFileService = cms.Service("TFileService",
    fileName = cms.string("hist.root"),
)

process.p = cms.Path(process.tpPoint)

#process.out = cms.OutputModule("PoolOutputModule",
#    fileName = cms.untracked.string("a.root"),
#    outputCommands = cms.untracked.vstring("drop *", "keep *_rpcPointFromTagProbe_*_RPCAnalysis"),
#)
#process.outPath = cms.EndPath(process.out)