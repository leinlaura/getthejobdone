from des import SchedulerDES
from process import Process, ProcessStates
from event import Event, EventTypes


class FCFS(SchedulerDES):
    def scheduler_func(self, cur_event):
        """ since the only event the scheduler is called with in FCFS is a process
        arring, return the process associated with the event"""
        return self.processes[cur_event.process_id]

    def dispatcher_func(self, cur_process):
        cur_process.process_state = ProcessStates.RUNNING #set state to RUNNING
        cur_process.run_for(cur_process.service_time, self.time) #run for the entire service time of process
        cur_process.process_state = ProcessStates.TERMINATED #terminate process
        new_event = Event(process_id= cur_process.process_id, event_type = EventTypes.PROC_CPU_DONE,
                          event_time = cur_process.departure_time) #create PROC_CPU_DONE event
        return new_event


class SJF(SchedulerDES):
    def scheduler_func(self, cur_event):
        ready_proc = []
        """iterate through list of processes, addd those that are
        in the READY state to a list"""
        for process in self.processes:
            if process.process_state == ProcessStates.READY:
                ready_proc.append(process)
        ready_proc.sort(key = lambda x: x.service_time) #sort list by service time
        return ready_proc[0] #return first item in the sorted list (always the shortest)

    #dispatcher the same as FCFS
    def dispatcher_func(self, cur_process):
        cur_process.process_state = ProcessStates.RUNNING #set process state to RUNNING
        cur_process.run_for(cur_process.service_time, self.time) #run for the entire service time of process
        cur_process.process_state = ProcessStates.TERMINATED #terminate process
        new_event = Event(process_id= cur_process.process_id, event_type = EventTypes.PROC_CPU_DONE,
                          event_time = cur_process.departure_time) #create PROC_CPU_DONE event
        return new_event


class RR(SchedulerDES):
    #same as FCFS
    def scheduler_func(self, cur_event):
        return self.processes[cur_event.process_id]

    def dispatcher_func(self, cur_process):
        cur_process.process_state = ProcessStates.RUNNING #set process state to RUNNING
        run_time = cur_process.run_for(self.quantum, self.time) #run for quantum time, save actual running time in run_time
        
        """ if the actual running time is smaller than the quantum, this
        indicates that process is finished"""
        if run_time < self.quantum: 
            cur_process.process_state = ProcessStates.TERMINATED #set process state to TERMINATED
            new_event = Event(process_id= cur_process.process_id, event_type = EventTypes.PROC_CPU_DONE,
                              event_time = cur_process.departure_time) #create PROC_CPU_DONE event
            
        #if run_time is not smaller, process needs more time; a CPU required event is created
        else:
            cur_process.process_state = ProcessStates.READY #process set back to READY state
            new_event = Event(process_id= cur_process.process_id, event_type = EventTypes.PROC_CPU_REQ,
                              event_time = self.time + run_time) # create PROC_CPU_REQ event
        return new_event


class SRTF(SchedulerDES):
    #scheduling function is optimised for different context switch times
    def scheduler_func(self, cur_event):
        ready_proc = []
        cur_proc = self.process_on_cpu #current process on cpu
        """iterate through list of processes, add those that are
        in the READY state to a list"""
        for process in self.processes:
            if process.process_state == ProcessStates.READY:
                ready_proc.append(process)
        ready_proc.sort(key = lambda x: x.remaining_time) #sort by remaining time
        
        #following four lines of code are only relevant when the context switch time is not zero
        #checks if cur_process is either zero or not in ready state (so not in the list)
        if (cur_proc == None) or (cur_proc not in ready_proc):
            return ready_proc[0] #if that is the case, return the first of the list
        #checks if first process remaining time accounting for context switch time is bigger 
        elif ready_proc[0].remaining_time + self.context_switch_time > cur_proc.remaining_time:
            #if bigger than current remaining time of process on cpu, return the current process
            return cur_proc
        #in case context switch time = 0 or cur_proc.remaining time higher, return ready_proc[0]
        return ready_proc[0]
        
    def dispatcher_func(self, cur_process):
        cur_process.process_state = ProcessStates.RUNNING #set process state to RUNNING
        remainTime = cur_process.remaining_time #intial remaining time
        
        #run for time until next event occurs; store actual running time in run_time
        run_time = cur_process.run_for(self.next_event_time()-self.time, self.time)
        """ if the actual running time is smaller than the initial remaining time,
        process requires further CPU access"""
        if run_time < remainTime: 
            cur_process.process_state = ProcessStates.READY #set process state to READY
            new_event = Event(process_id= cur_process.process_id, event_type = EventTypes.PROC_CPU_REQ,
                      event_time = self.time + run_time) #create PROC_CPU_REQ event
            
        #otherwise process is done
        else:
            cur_process.process_state = ProcessStates.TERMINATED #set process state to TERMINATED
            new_event = Event(process_id= cur_process.process_id, event_type = EventTypes.PROC_CPU_DONE,
                              event_time = cur_process.departure_time) #create PROC_CPU_DONE event
        return new_event
            
      
      
      
      
      
      
