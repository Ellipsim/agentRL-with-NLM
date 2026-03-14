

(define (problem BW-rand-11)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 )
(:init
(arm-empty)
(on b1 b6)
(on b2 b5)
(on-table b3)
(on-table b4)
(on b5 b8)
(on-table b6)
(on b7 b4)
(on b8 b9)
(on b9 b3)
(on b10 b7)
(on b11 b10)
(clear b1)
(clear b2)
(clear b11)
)
(:goal
(and
(on b1 b7)
(on b2 b3)
(on b3 b10)
(on b5 b2)
(on b6 b9)
(on b8 b11)
(on b9 b5))
)
)


