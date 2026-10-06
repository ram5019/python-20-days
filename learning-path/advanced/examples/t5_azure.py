"""Track 5c example: Azure SDK for Python (READ-ONLY).

Run:    python3 learning-path/advanced/examples/t5_azure.py [--subscription <id>]
Needs:  pip install azure-identity azure-mgmt-resource azure-mgmt-resource-subscriptions azure-mgmt-compute
Login (any ONE of these; the code never contains secrets):
          az login                                    (easiest for learning)
          environment variables AZURE_CLIENT_ID / AZURE_TENANT_ID / AZURE_CLIENT_SECRET
          a managed identity when running inside Azure

This script only LISTS things. It creates, changes and deletes nothing.
"""

import argparse
import os

from azure.core.exceptions import ClientAuthenticationError, HttpResponseError
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource.resources import ResourceManagementClient
from azure.mgmt.resource.subscriptions import SubscriptionClient


# BLOCK 1: ONE credential object, reused by every client.
# DefaultAzureCredential tries several login methods in order and uses the first that works.
def make_credential():
    return DefaultAzureCredential()


# BLOCK 2: subscriptions: the billing/organisation boundary everything lives under
def list_subscriptions(credential):
    client = SubscriptionClient(credential)
    return [(s.subscription_id, s.display_name, s.state) for s in client.subscriptions.list()]


# BLOCK 3: resource groups: folders that hold related resources
def list_resource_groups(credential, subscription_id):
    client = ResourceManagementClient(credential, subscription_id)
    return [(g.name, g.location) for g in client.resource_groups.list()]


# BLOCK 4: virtual machines
def list_vms(credential, subscription_id):
    client = ComputeManagementClient(credential, subscription_id)
    vms = []
    for vm in client.virtual_machines.list_all():     # the SDK pages through results for you
        vms.append({
            "name": vm.name,
            "location": vm.location,
            "size": vm.hardware_profile.vm_size if vm.hardware_profile else None,
            "resource_group": resource_group_from_id(vm.id),
            "tags": vm.tags or {},
        })
    return vms


# BLOCK 5: pure helper: resource IDs are paths like
#   /subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.Compute/virtualMachines/<name>
def resource_group_from_id(resource_id):
    parts = resource_id.strip("/").split("/")
    lowered = [p.lower() for p in parts]
    if "resourcegroups" in lowered:
        return parts[lowered.index("resourcegroups") + 1]
    return None


# BLOCK 6: pure logic on the data (easy to test; Day 20 layering)
def group_by_location(vms):
    groups = {}
    for vm in vms:
        groups.setdefault(vm["location"], []).append(vm["name"])
    return groups


def main():
    parser = argparse.ArgumentParser(description="Read-only Azure overview")
    parser.add_argument("--subscription", default=os.environ.get("AZURE_SUBSCRIPTION_ID"))
    args = parser.parse_args()

    try:
        cred = make_credential()
        subs = list_subscriptions(cred)
        print(f"Subscriptions ({len(subs)}):")
        for sub in subs:
            print("  ", sub)

        sub_id = args.subscription or (subs[0][0] if subs else None)
        if not sub_id:
            print("No subscription available.")
            return
        print("\nUsing subscription:", sub_id)
        print("Resource groups:", list_resource_groups(cred, sub_id)[:10])
        vms = list_vms(cred, sub_id)
        print(f"VMs: {len(vms)}")
        for vm in vms[:10]:
            print("  ", vm)
        print("By location:", group_by_location(vms))
    except ClientAuthenticationError:
        print("Not logged in to Azure. Run `az login`, or set the AZURE_* environment variables.")
    except HttpResponseError as e:
        print(f"Azure rejected the request ({e.status_code}): {e.message}")


if __name__ == "__main__":
    main()
