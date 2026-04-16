(set-logic ALL)
; Constraint ID: b557075fecc84e8f
; Generated at: 2026-04-16 11:54:14
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60601)) (False)
(assert (not (= x 60601)))

; Query: ((== x 60602)) (False)
(assert (not (not (= x 60602))))

(check-sat)
(get-model)
