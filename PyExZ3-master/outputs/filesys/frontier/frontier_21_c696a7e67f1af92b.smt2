(set-logic ALL)
; Constraint ID: c696a7e67f1af92b
; Generated at: 2026-04-16 11:43:57
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60316)) (False)
(assert (not (= x 60316)))

; Query: ((== x 60317)) (False)
(assert (not (not (= x 60317))))

(check-sat)
(get-model)
