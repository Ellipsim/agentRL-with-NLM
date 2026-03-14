

(define (problem BW-rand-12)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 )
(:init
(arm-empty)
(on b1 b11)
(on b2 b5)
(on b3 b1)
(on b4 b6)
(on b5 b9)
(on-table b6)
(on-table b7)
(on b8 b4)
(on b9 b3)
(on b10 b12)
(on-table b11)
(on b12 b2)
(clear b7)
(clear b8)
(clear b10)
)
(:goal
(and
(on b1 b11)
(on b2 b7)
(on b4 b12)
(on b5 b10)
(on b7 b9)
(on b8 b4)
(on b9 b6)
(on b10 b8)
(on b11 b3))
)
)


