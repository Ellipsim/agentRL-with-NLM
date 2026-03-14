

(define (problem BW-rand-12)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 )
(:init
(arm-empty)
(on-table b1)
(on-table b2)
(on b3 b10)
(on b4 b7)
(on b5 b8)
(on-table b6)
(on b7 b6)
(on b8 b3)
(on-table b9)
(on b10 b12)
(on b11 b9)
(on b12 b1)
(clear b2)
(clear b4)
(clear b5)
(clear b11)
)
(:goal
(and
(on b1 b11)
(on b3 b4)
(on b4 b10)
(on b5 b6)
(on b8 b12)
(on b9 b7)
(on b10 b1)
(on b11 b9)
(on b12 b3))
)
)


