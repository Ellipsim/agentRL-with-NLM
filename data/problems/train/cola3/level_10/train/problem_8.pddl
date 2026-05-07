

(define (problem BW-rand-11)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 - block)
(:init
(handempty)
(ontable b1)
(on b2 b10)
(ontable b3)
(on b4 b3)
(ontable b5)
(on b6 b4)
(on b7 b5)
(on b8 b11)
(on b9 b1)
(on b10 b7)
(on b11 b9)
(clear b2)
(clear b6)
(clear b8)
)
(:goal
(and
(on b3 b2)
(on b4 b5)
(on b5 b10)
(on b6 b3)
(on b7 b8)
(on b8 b1)
(on b11 b4))
)
)


