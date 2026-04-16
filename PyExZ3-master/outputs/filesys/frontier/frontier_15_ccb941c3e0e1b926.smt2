(set-logic ALL)
; Constraint ID: ccb941c3e0e1b926
; Generated at: 2026-04-16 11:42:36
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60232)) (False)
(assert (not (= x 60232)))

; Query: ((== x 60233)) (False)
(assert (not (not (= x 60233))))

(check-sat)
(get-model)
