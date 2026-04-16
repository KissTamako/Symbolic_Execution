(set-logic ALL)
; Path ID: bc649be9cf391613
; Generated at: 2026-04-16 12:01:22
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const c Int)
(declare-const se Int)


; Query: ((== (+ 3 c) 6)) (False)
(assert (not (not (= (+ 3 c) 6))))

(check-sat)
(get-model)
