(set-logic ALL)
; Frontier Constraint ID: 254567e159d52eec
; Generated at: 2026-04-16 15:10:06
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1042)) (False)
(assert (not (not (= x 1042))))

(check-sat)
(get-model)
