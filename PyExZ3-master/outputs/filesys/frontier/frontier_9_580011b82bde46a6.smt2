(set-logic ALL)
; Constraint ID: 580011b82bde46a6
; Generated at: 2026-04-16 11:49:33
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60448)) (False)
(assert (not (= x 60448)))

; Query: ((== x 60449)) (False)
(assert (not (not (= x 60449))))

(check-sat)
(get-model)
