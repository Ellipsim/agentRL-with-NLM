

(define (problem BW-rand-13)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 )
(:init
(arm-empty)
(on b1 b9)
(on b2 b11)
(on-table b3)
(on b4 b8)
(on-table b5)
(on b6 b13)
(on b7 b2)
(on b8 b3)
(on b9 b5)
(on b10 b7)
(on b11 b4)
(on b12 b1)
(on-table b13)
(clear b6)
(clear b10)
(clear b12)
)
(:goal
(and
(on b2 b6)
(on b4 b1)
(on b5 b2)
(on b6 b13)
(on b8 b7)
(on b9 b3)
(on b10 b8)
(on b11 b9)
(on b12 b10))
)
)


