

(define (problem BW-rand-11)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 )
(:init
(arm-empty)
(on-table b1)
(on-table b2)
(on b3 b10)
(on-table b4)
(on b5 b3)
(on b6 b1)
(on-table b7)
(on b8 b2)
(on b9 b8)
(on b10 b9)
(on b11 b7)
(clear b4)
(clear b5)
(clear b6)
(clear b11)
)
(:goal
(and
(on b1 b4)
(on b2 b7)
(on b4 b8)
(on b5 b3)
(on b6 b10)
(on b7 b11)
(on b8 b5)
(on b9 b6)
(on b10 b1)
(on b11 b9))
)
)


