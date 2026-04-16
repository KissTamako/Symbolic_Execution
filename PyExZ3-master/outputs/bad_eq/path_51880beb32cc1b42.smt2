(set-logic ALL)
; Path ID: 51880beb32cc1b42
; Generated at: 2026-04-16 12:01:19
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const i Int)
(declare-const se Int)


; Query: ((== i 0)) (False)
(assert (not (not (= i 0))))

(check-sat)
(get-model)
