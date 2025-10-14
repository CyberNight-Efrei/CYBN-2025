1. Constater la présence répétitive de réception de signaux linux

ex:

```
--- SIGUSR1 {si_signo=SIGUSR1, si_code=SI_USER, si_pid=15584, si_uid=1000} ---
--- SIGCONT {si_signo=SIGCONT, si_code=SI_USER, si_pid=15584, si_uid=1000} ---
rt_sigreturn({mask=[USR1]})             = 0
rt_sigreturn({mask=[]})                 = -1 EINTR (Interrupted system call)
pause()                                 = ? ERESTARTNOHAND (To be restarted if no handler)
--- SIGUSR1 {si_signo=SIGUSR1, si_code=SI_USER, si_pid=15584, si_uid=1000} ---
rt_sigreturn({mask=[]})                 = -1 EINTR (Interrupted system call)
pause()                                 = ? ERESTARTNOHAND (To be restarted if no handler)
--- SIGUSR1 {si_signo=SIGUSR1, si_code=SI_USER, si_pid=15584, si_uid=1000} ---
rt_sigreturn({mask=[]})                 = -1 EINTR (Interrupted system call)
pause()                                 = ? ERESTARTNOHAND (To be restarted if no handler)
--- SIGUSR1 {si_signo=SIGUSR1, si_code=SI_USER, si_pid=15584, si_uid=1000} ---
rt_sigreturn({mask=[]})                 = -1 EINTR (Interrupted system call)
pause()                                 = ? ERESTARTNOHAND (To be restarted if no handler)
--- SIGUSR1 {si_signo=SIGUSR1, si_code=SI_USER, si_pid=15584, si_uid=1000} ---
rt_sigreturn({mask=[]})                 = -1 EINTR (Interrupted system call)
pause()                                 = ? ERESTARTNOHAND (To be restarted if no handler)
--- SIGUSR1 {si_signo=SIGUSR1, si_code=SI_USER, si_pid=15584, si_uid=1000} ---
rt_sigreturn({mask=[]})                 = -1 EINTR (Interrupted system call)
pause()                                 = ? ERESTARTNOHAND (To be restarted if no handler)
--- SIGUSR1 {si_signo=SIGUSR1, si_code=SI_USER, si_pid=15584, si_uid=1000} ---
rt_sigreturn({mask=[]})                 = -1 EINTR (Interrupted system call)
```

2. Isoler chaque signal

ex:

```
❯ rg si_signo logs.txt | cut -d " " -f 2
SIGUSR1
SIGCONT
SIGUSR1
SIGUSR1
SIGUSR1
SIGUSR1
```

3. Constater que SIGUSR1 et SIGUSR2 sont majoritaires, les transformer en 0 et 1

4. Passer le tout dans cyberchef : 

> file:///home/arch/Tools/CyberChef/build/prod/index.html#recipe=From_Binary('Space',8)&input=MApTSUdDT05UCjAKMAowCjAKMAowCjAKMAowCjAKMAowCjAKMAowCjAKMAowCjAKMAowCjAKMAowCjAKMQowCjAKMQowCjEKU0lHQ09OVAowCjEKMAowCjAKMAoxCjEKMAoxCjAKMQoxCjAKMAoxCjAKMQowCjAKMAowCjEKMAowCjEKMAowCjEKMQoxCjAKMAoxCjEKMQoxCjAKMQoxCjAKMQowCjEKMAoxCjEKMQowCjEKMQowCjEKMAowCjAKMAowCjEKMQowCjEKMAowCjAKMQoxCjEKMAoxCjAKMAowCjEKMAoxCjEKMQoxCjEKMAowCjEKMQowCjEKMAowCjAKMQowCjEKMQoxCjEKMQowCjEKMAoxCjAKMQoxCjEKMAowCjEKMQowCjAKMQoxCjAKMAoxCjEKMAowCjAKMQowCjEKMQoxCjAKMAoxCjAKMAoxCjEKMAowCjEKMAowCjAKMQowCjEKMQoxCjEKMQowCjEKMAoxCjAKMQoxCjEKMAowCjEKMQowCjEKMAowCjAKMQoxCjEKMQowCjAKMQowCjEKMAoxCjEKMQoxCjEKMAoxCjAKMQowCjEKMAowCjAKMAoxCjEKMAowCjAKMAowCjEKMAoxCjEKMQoxCjEKMAoxCjAKMAowCjAKMQoxCjAKMAoxCjEKMAowCjAKMAowCjEKMQowCjEKMQowCjEKMAoxCjEKMAoxCjEKMAoxCjAKMQoxCjEKMAoxCjAKMQowCjEKMQowCjEKMQoxCjAKMAowCjEKMQowCjAKMAoxCjAKMQoxCjAKMAowCjEKMQowCjAKMQoxCjAKMQowCjAKMAoxCjEKMQowCjEKMAowCjAKMAoxCjEKMAowCjEKMQowCjEKMQoxCjEKMQowCjEKU0lHVEVSTQpTSUdJTlQK

Cleanup les SIGCONT, SIGTERM, ...

> flag: CYBN{Wh4t_4_W31rd_W4y_T0_C0mmun1c4t3}

> cf : file:///home/arch/Tools/CyberChef/build/prod/index.html#recipe=From_Binary('Space',8)&input=MAowCjAKMAowCjAKMAowCjAKMAowCjAKMAowCjAKMAowCjAKMAowCjAKMAowCjAKMAowCjEKMAowCjEKMAoxCjAKMQowCjAKMAowCjEKMQowCjEKMAoxCjEKMAowCjEKMAoxCjAKMAowCjAKMQowCjAKMQowCjAKMQoxCjEKMAowCjEKMQoxCjEKMAoxCjEKMAoxCjAKMQowCjEKMQoxCjAKMQoxCjAKMQowCjAKMAowCjAKMQoxCjAKMQowCjAKMAoxCjEKMQowCjEKMAowCjAKMQowCjEKMQoxCjEKMQowCjAKMQoxCjAKMQowCjAKMAoxCjAKMQoxCjEKMQoxCjAKMQowCjEKMAoxCjEKMQowCjAKMQoxCjAKMAoxCjEKMAowCjEKMQowCjAKMAoxCjAKMQoxCjEKMAowCjEKMAowCjEKMQowCjAKMQowCjAKMAoxCjAKMQoxCjEKMQoxCjAKMQowCjEKMAoxCjEKMQowCjAKMQoxCjAKMQowCjAKMAoxCjEKMQoxCjAKMAoxCjAKMQowCjEKMQoxCjEKMQowCjEKMAoxCjAKMQowCjAKMAowCjEKMQowCjAKMAowCjAKMQowCjEKMQoxCjEKMQowCjEKMAowCjAKMAoxCjEKMAowCjEKMQowCjAKMAowCjAKMQoxCjAKMQoxCjAKMQowCjEKMQowCjEKMQowCjEKMAoxCjEKMQowCjEKMAoxCjAKMQoxCjAKMQoxCjEKMAowCjAKMQoxCjAKMAowCjEKMAoxCjEKMAowCjAKMQoxCjAKMAoxCjEKMAoxCjAKMAowCjEKMQoxCjAKMQowCjAKMAowCjEKMQowCjAKMQoxCjAKMQoxCjEKMQoxCjAKMQo