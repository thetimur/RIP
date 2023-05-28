import json
import RIPEmulator as r

input_data = json.load(open('RIP_INPUT.json'))
output_data = open("RIP_RESULT.txt", "w")

graphs = [r.RIPEmulator(name, input_data[name]) for name in input_data]

idx = 1
continues = True

# RIP
while continues:
    continues = False

    for i, router1 in enumerate(graphs):
        for j, router2 in enumerate(graphs):
            if i == j:
                continue

            for r1 in router1.connections:
                metric = int(1e9)
                stop = False

                if r1 in router2.metrics:
                    metric = router2.metrics[r1]

                can_update = (router2.address not in router1.metrics or 1 + metric <
                              router1.metrics[router2.address]) and not metric == int(1e9)
                if can_update:
                    router1.metrics[router2.address] = 1 + metric
                    router1.next[router2.address] = r1

                    stop = True

                continues |= stop

        output_data.write(f'Step {idx} [{router1.address}]\n\n')
        output_data.write(
            f'{"|Source|":17} {"|Destination|":17} {"|Next Hop|":18} {"|Metric|":10}\n')

        for target in router1.metrics:
            output_data.write(
                f'{router1.address:17} {target:16} {router1.next[target]:22} {str(router1.metrics[target]):1}\n')
        output_data.write('\n* End *\n\n\n')
    idx += 1


# Result
for router in graphs:
    output_data.write(
        f'[{router.address}]\n{"|Source|":17} {"|Destination|":17} {"|Next Hop|":18} {"|Metric|":10}\n')

    for target in router.metrics:
        output_data.write(
            f'{router.address:17} {target:16} {router.next[target]:22} {str(router.metrics[target]):1}\n')

    output_data.write('\n')

output_data.close()
