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
#include "veins/base/utils/Coord.h"
#include "veins/modules/mobility/traci/TraCIScenarioManager.h"
#include "veins/modules/mobility/traci/TraCIScenarioManagerLaunchd.h"
#include <vector>

using namespace omnetpp;


class MapChecker : public cSimpleModule
{
    private:
        std::vector<Coord> coordinates;
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
    cModule * car = getParentModule();
    std::string display = std::string(car->getDisplayString().str());
    std::string coordString = display.substr(2,display.find(";")-2);
    double x = std::stod(coordString.substr(0,coordString.find(",")-2));
    double y = std::stod(coordString.substr(coordString.find(",")+1));
    Coord checkedCoord = Coord(x,y,0);

    if (coordinates.empty() || checkedCoord.distance(coordinates.back())>3){
        coordinates.push_back(checkedCoord);
    }

    //this->getParentNode()->getSub
    // Increment counter and check value.
    EV<<"MapChecker Message received\n";



}

