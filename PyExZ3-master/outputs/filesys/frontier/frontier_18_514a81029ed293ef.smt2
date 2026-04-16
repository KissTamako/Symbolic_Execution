(set-logic ALL)
; Frontier Constraint ID: 514a81029ed293ef
; Generated at: 2026-04-16 15:26:57
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1339)) (False)
(assert (not (not (= x 1339))))

(check-sat)
(get-model)
