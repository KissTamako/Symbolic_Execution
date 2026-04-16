(set-logic ALL)
; Frontier Constraint ID: 464cb83934652b1e
; Generated at: 2026-04-16 14:41:51
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 508)) (False)
(assert (not (not (= x 508))))

(check-sat)
(get-model)
