(set-logic ALL)
; Frontier Constraint ID: fca318a7d496db1d
; Generated at: 2026-04-16 13:27:43
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const a Int)


; Query: ((< a 0)) (False)
(assert (not (not (< a 0))))

(check-sat)
(get-model)
