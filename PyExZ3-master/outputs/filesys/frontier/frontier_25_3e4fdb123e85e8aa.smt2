(set-logic ALL)
; Constraint ID: 3e4fdb123e85e8aa
; Generated at: 2026-04-16 11:28:21
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59947)) (False)
(assert (not (= x 59947)))

; Query: ((== x 59948)) (False)
(assert (not (not (= x 59948))))

(check-sat)
(get-model)
