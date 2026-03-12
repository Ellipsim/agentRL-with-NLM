

(define (problem BW-rand-13)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 )
(:init
(arm-empty)
(on-table b1)
(on b2 b11)
(on b3 b4)
(on b4 b12)
(on b5 b10)
(on b6 b3)
(on-table b7)
(on b8 b9)
(on b9 b5)
(on b10 b6)
(on b11 b8)
(on b12 b13)
(on-table b13)
(clear b1)
(clear b2)
(clear b7)
)
(:goal
(and
(on b2 b12)
(on b4 b2)
(on b5 b11)
(on b6 b1)
(on b7 b9)
(on b8 b7)
(on b10 b8)
(on b11 b10)
(on b12 b5))
)
)


