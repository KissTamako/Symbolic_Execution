(set-logic ALL)
; Frontier Constraint ID: dec49335abe05678
; Generated at: 2026-04-16 14:41:51
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 514)) (False)
(assert (not (not (= x 514))))

(check-sat)
(get-model)
