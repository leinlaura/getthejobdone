print(cur_event)
        queue = []
        for event in self.events_queue:
cur_process = self.processes[event.process_id]
            if (event.event_type == EventTypes.PROC_ARRIVES) and (event.event_time <= self.time) and (cur_process.process_state == ProcessStates.READY):
                queue.append(event)
        queue.sort(key= lambda x: self.processes[x.process_id].service_time)
        if len(queue) == 0:
            print(self.processes[cur_event.process_id].process_state)
            print(self.processes[cur_event.process_id].process_id)
            return self.processes[cur_event.process_id]
        print(self.processes[queue[0].process_id].process_id)
        return self.processes[queue[0].process_id]
