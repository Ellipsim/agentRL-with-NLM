

(define (problem BW-rand-11)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 )
(:init
(arm-empty)
(on-table b1)
(on b2 b3)
(on b3 b8)
(on-table b4)
(on b5 b9)
(on b6 b11)
(on b7 b2)
(on-table b8)
(on b9 b7)
(on b10 b5)
(on-table b11)
(clear b1)
(clear b4)
(clear b6)
(clear b10)
)
(:goal
(and
(on b2 b3)
(on b4 b6)
(on b5 b2)
(on b6 b11)
(on b7 b9)
(on b9 b8)
(on b10 b5))
)
)


