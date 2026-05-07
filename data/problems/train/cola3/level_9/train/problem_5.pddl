

(define (problem BW-rand-11)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 - block)
(:init
(handempty)
(on b1 b4)
(ontable b2)
(on b3 b7)
(ontable b4)
(on b5 b10)
(ontable b6)
(on b7 b8)
(on b8 b6)
(ontable b9)
(ontable b10)
(on b11 b2)
(clear b1)
(clear b3)
(clear b5)
(clear b9)
(clear b11)
)
(:goal
(and
(on b1 b4)
(on b2 b9)
(on b3 b7)
(on b5 b2)
(on b6 b10)
(on b8 b1)
(on b10 b3)
(on b11 b5))
)
)


