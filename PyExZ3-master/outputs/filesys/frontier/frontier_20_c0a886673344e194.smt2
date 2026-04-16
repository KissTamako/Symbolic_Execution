(set-logic ALL)
; Frontier Constraint ID: c0a886673344e194
; Generated at: 2026-04-16 15:16:56
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1192)) (False)
(assert (not (not (= x 1192))))

(check-sat)
(get-model)
