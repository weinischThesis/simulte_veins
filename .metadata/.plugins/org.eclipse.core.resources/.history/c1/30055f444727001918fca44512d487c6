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
#include <iostream>
#include <iomanip>
#include <fstream>
#include "veins_inet/VeinsInetMobility.h"
#include "veins_inet/VeinsInetManager.h"
#include "veins/modules/mobility/traci/TraCIConnection.h"
#include "veins/modules/mobility/traci/TraCICoord.h"

using namespace omnetpp;


class MapChecker : public cSimpleModule
{
    private:
        std::vector<inet::Coord> coordinates;
    protected:
        virtual void initialize() override;
        virtual void handleMessage(cMessage *msg) override;
        virtual void finish() override;
};
Define_Module(MapChecker);



void MapChecker::initialize()
{


    EV <<"initialize MapChecker\n";


}

void MapChecker::handleMessage(cMessage *msg)
{

    cModule * car = getParentModule();
    cModule * mobilityMod = car->getSubmodule("mobility");
    Veins::VeinsInetMobility *inetmm = dynamic_cast<Veins::VeinsInetMobility*>(mobilityMod);
    inet::Coord checkedCoord = inetmm->getCurrentPosition();

    /*std::string display = std::string(car->getDisplayString().str());
    std::string coordString = display.substr(2,display.find(";")-2);
    double x = std::stod(coordString.substr(0,coordString.find(",")-2));
    double y = std::stod(coordString.substr(coordString.find(",")+1));
    Coord checkedCoord = Coord(x,y,0);
*/
    if (coordinates.empty() || checkedCoord.distance(coordinates.back())>3){
        coordinates.push_back(checkedCoord);
    }
    //this->getParentNode()->getSub
    // Increment counter and check value.
    EV<<"MapChecker Message received\n";
}

void MapChecker::finish()
{
    cModule * car = getParentModule();
    std::string filename = "workingCoordinates/"+std::string(car->getFullName())+".txt";
    std::ofstream file;
   // Veins::VeinsInetManager * veinsm = Veins::VeinsInetManagerAccess.get();
    Veins::TraCIScenarioManager* tracim = Veins::TraCIScenarioManagerAccess().get();
    Veins::TraCIConnection* connection = tracim->getConnection();
    file.open(filename.c_str());
    for (auto &coord : coordinates)
    {
        Coord omCoord = Coord(coord.x,coord.y,coord.z);
        Veins::TraCICoord traciCoord = connection->omnet2traci(omCoord);

        file << std::fixed << std::setprecision(2) << traciCoord.x << "," << std::fixed << std::setprecision(2) << traciCoord.y <<"\n";
    }
    file.close();
}



