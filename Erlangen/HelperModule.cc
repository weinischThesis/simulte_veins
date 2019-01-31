//
// This file is part of an OMNeT++/OMNEST simulation example.
//
// Copyright (C) 1992-2015 Andras Varga
//
// This file is distributed WITHOUT ANY WARRANTY. See the file
// `license' for details on this and other legal matters.
//


#include <string.h>
#include <omnetpp.h>
#include <string>
#include "veins/modules/mobility/traci/TraCIScenarioManager.h"
#include "veins/modules/mobility/traci/TraCIScenarioManagerLaunchd.h"

using namespace omnetpp;


class HelperModule : public cSimpleModule
{
    protected:
        virtual void initialize() override;
        virtual void updateEnodesFromSumoToOmnet(omnetpp::cModule * module,int numOfEnodeBs);
};
Define_Module(HelperModule);



void HelperModule::initialize()
{
    cModule * erlangenModule = getParentModule();
    std::string modName = Veins::TraCIScenarioManagerLaunchdAccess().get()->par("moduleName");

    const char * moduleName = modName.c_str();
    //updateEnodesFromSumoToOmnet(erlangenModule,2);

    //std::string nodeType = eNodeB->par("nodeType");

    EV << moduleName <<"12345\n";


}

void HelperModule::updateEnodesFromSumoToOmnet(cModule * erlangen,int numOfEnodeBs){
    for (int i=1;i<=numOfEnodeBs;i++){
        std::string id = "eNodeB"+std::to_string(i);

        const char * nodeName = id.c_str();
        EV << nodeName;
        cModule * eNodeB = erlangen->getSubmodule(nodeName);

        //cModule * eNodeB = erlangen->getSubmodule(nodeName)->getSubmodule("mobility")->par("initialX");
        //std::string initialX = std::to_string(erlangen->getSubmodule(nodeName)->getSubmodule("mobility")->par("initialX"));


      //  const char * inX = initialX.c_str();
    //   EV << " x: " << inX;
    }
}


