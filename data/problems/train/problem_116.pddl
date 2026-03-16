

(define (problem BW-rand-11)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 - block)
(:init
(handempty)
(on b1 b11)
(on b2 b10)
(on b3 b8)
(on b4 b5)
(ontable b5)
(on b6 b4)
(ontable b7)
(on b8 b9)
(on b9 b6)
(on b10 b3)
(ontable b11)
(clear b1)
(clear b2)
(clear b7)
)
(:goal
(and
(on b1 b6)
(on b2 b5)
(on b3 b11)
(on b5 b4)
(on b6 b2)
(on b7 b1)
(on b8 b7)
(on b9 b3)
(on b11 b8))
)
)


