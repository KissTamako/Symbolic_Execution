(set-logic ALL)
; Constraint ID: c55822b6d1610615
; Generated at: 2026-04-16 11:42:36
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60217)) (False)
(assert (not (= x 60217)))

; Query: ((== x 60218)) (False)
(assert (not (not (= x 60218))))

(check-sat)
(get-model)
