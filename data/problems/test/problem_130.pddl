

(define (problem BW-rand-11)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 - block)
(:init
(handempty)
(on b1 b8)
(ontable b2)
(on b3 b11)
(on b4 b3)
(ontable b5)
(ontable b6)
(on b7 b4)
(on b8 b6)
(on b9 b1)
(on b10 b2)
(ontable b11)
(clear b5)
(clear b7)
(clear b9)
(clear b10)
)
(:goal
(and
(on b1 b9)
(on b2 b1)
(on b3 b11)
(on b4 b5)
(on b6 b4)
(on b7 b8)
(on b9 b3)
(on b10 b6)
(on b11 b7))
)
)


