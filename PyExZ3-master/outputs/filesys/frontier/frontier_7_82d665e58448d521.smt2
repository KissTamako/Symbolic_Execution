(set-logic ALL)
; Constraint ID: 82d665e58448d521
; Generated at: 2026-04-16 11:42:36
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60220)) (False)
(assert (not (= x 60220)))

; Query: ((== x 60221)) (False)
(assert (not (not (= x 60221))))

(check-sat)
(get-model)
