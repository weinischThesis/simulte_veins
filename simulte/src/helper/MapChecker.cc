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


class MapChecker : public cSimpleModule
{
    protected:
        virtual void initialize() override;
        virtual void handleMessage(cMessage *msg) override;
};
Define_Module(MapChecker);



void MapChecker::initialize()
{


    EV <<"initialize MapChecker\n";


}

void MapChecker::handleMessage(cMessage *msg)
{
    // Increment counter and check value.
    EV<<"MapChecker Message received\n";
}

