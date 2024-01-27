#!/usr/bin/env python3

from waapi import WaapiClient, CannotConnectToWaapiException
import sys, re, os, argparse

# Define arguments for the script
parser = argparse.ArgumentParser(description='Auto-rename container for the specified Wwise object ID.')
parser.add_argument('id', metavar='GUID', nargs='?', help='One guid of the form {01234567-89ab-cdef-0123-4567890abcde}. The script retrieves the current selected if no GUID specified.')

args = parser.parse_args()
try:
    # Connecting to Waapi using default URL
    with WaapiClient() as client:

        if args.id is None:
            selected  = client.call("ak.wwise.ui.getSelectedObjects")['objects']

            for i in range(len(selected)):
                args.id = selected[i]['id']
            
                get_args = {
                    "from": {"id": [args.id]},
                    "transform": [
                        {"select": ['ancestors']}
                    ]
                }
                options = {
                    "return": ['name']
                }
                ancestors = client.call("ak.wwise.core.object.get", get_args, options=options)['return']
                
                ancestorsLength = len(ancestors)
                dialogueEvent = ancestors[ancestorsLength - 4]['name']
                culture = ancestors[ancestorsLength - 5]['name']
                creator = ancestors[ancestorsLength - 6]['name']
                unit = ancestors[ancestorsLength - 7]['name']
                unitSubcategory = ancestors[ancestorsLength - 8]['name']
                unitSubcategory2 = ancestors[ancestorsLength - 9]['name']

                if ancestorsLength == 9:
                    print("ancestorsLength: " + str(ancestorsLength))
                    if dialogueEvent == 'Actor-Mixer Hierarchy' or culture == 'Actor-Mixer Hierarchy' or creator == 'Actor-Mixer Hierarchy' or unit == 'Actor-Mixer Hierarchy' or unitSubcategory == 'Actor-Mixer Hierarchy' or unitSubcategory2 == 'Actor-Mixer Hierarchy':
                        print("Whoops, something is wrong with the path...")
                    else:
                        randomContainerName = (dialogueEvent + "_" + culture + "_" + creator + "_" + unit + "_" + unitSubcategory + "_" + unitSubcategory2)
                        print("Renaming to: " + str(randomContainerName))
                        setNameArgs = {
                            "object": args.id,
                            "value":randomContainerName
                        }
                        client.call("ak.wwise.core.object.setName", setNameArgs)

                elif ancestorsLength == 8:
                    print("ancestorsLength: " + str(ancestorsLength))
                    if dialogueEvent == 'Actor-Mixer Hierarchy' or culture == 'Actor-Mixer Hierarchy' or creator == 'Actor-Mixer Hierarchy' or unit == 'Actor-Mixer Hierarchy' or unitSubcategory == 'Actor-Mixer Hierarchy':
                        print("Whoops, something is wrong with the path...")
                    else:
                        randomContainerName = (dialogueEvent + "_" + culture + "_" + creator + "_" + unit + "_" + unitSubcategory)
                        print("Renaming to: " + str(randomContainerName))
                        setNameArgs = {
                            "object": args.id,
                            "value":randomContainerName
                        }
                        client.call("ak.wwise.core.object.setName", setNameArgs)

                elif ancestorsLength == 7:
                    print("ancestorsLength: " + str(ancestorsLength))
                    if dialogueEvent == 'Actor-Mixer Hierarchy' or culture == 'Actor-Mixer Hierarchy' or creator == 'Actor-Mixer Hierarchy' or unit == 'Actor-Mixer Hierarchy':
                        print("Whoops, something is wrong with the path...")
                    else:
                        randomContainerName = (dialogueEvent + "_" + culture + "_" + creator + "_" + unit)
                        print("Renaming to: " + str(randomContainerName))
                        setNameArgs = {
                            "object": args.id,
                            "value":randomContainerName
                        }
                        client.call("ak.wwise.core.object.setName", setNameArgs)

                elif ancestorsLength == 6:
                    print("ancestorsLength: " + str(ancestorsLength))
                    if dialogueEvent == 'Actor-Mixer Hierarchy' or culture == 'Actor-Mixer Hierarchy' or creator == 'Actor-Mixer Hierarchy':
                        print("Whoops, something is wrong with the path...")
                    else:
                        randomContainerName = (dialogueEvent + "_" + culture + "_" + creator)
                        print("Renaming to: " + str(randomContainerName))
                        setNameArgs = {
                            "object": args.id,
                            "value":randomContainerName
                        }
                        client.call("ak.wwise.core.object.setName", setNameArgs)

                elif ancestorsLength < 6 or ancestorsLength > 9:
                    print("ancestorsLength: " + str(ancestorsLength))
                    print("Whoops, path cannot be less than 6 folders or greater than 9 folders...")

except CannotConnectToWaapiException:
    print("Could not connect to Waapi: Is Wwise running and Wwise Authoring API enabled?")

except Exception as e:
    print(str(e))
